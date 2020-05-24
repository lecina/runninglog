import datetime
import re
import numbers
import sys
import logging

import pandas as pd

from runninglog.constants import blockNames
from runninglog.utilities import utilities
from runninglog.run import segment, types
from runninglog.io import parser


class SingleRun():
    """Running activity object.

    A SingleRun is a running activity object.

    Attributes that must be defined:
        * Time
        * Distance
        * Date

    Ideally defined. Assigned default values otherwise:
        * Type (see note below)
        * Climb
        * Location (`where`)
        * Route
        * Trail
        * Feeling
        * Structure (`structure`)

    Units:
        * distance: km
        * time: min
        * pace: sec/km
        * climb: m
        * vspeed: m/h


    Note:
        The SingleRun type and Segment type refer to different concepts:\
        the former is a short identifier of the primary goal of the workout,\
        whereas the latter identifies the running intensities (e.g. easy\
        pace, marathon pace, threshold pace, interval/hard pace or repetition\
        in Daniel's running formula):

        * The SingleRun type expresses succintly the goal of the run and is\
        used as a quick identifier of workout type (e.g. easy run, interval\
        workout or race). Beside, the type is used to identify cross training\
        activities.

        * Segment types are used to classify training volume into the defined\
        running intensities. This is useful for example to keep\
        track of accumulated volume at each intensity or to compare\
        performance over time.

        * The user is expected to define the volume spent on each Segment\
        type in the structure section. When it does not cover the overall\
        time or distance (e.g. when no structure is defined), SingleRun\
        guesses the volume spent on each segment.

    """
    def __init__(self):
        self.type = None
        self.is_trail_running = False
        self.distance = 0
        self.time = None
        self.pace = None
        self.climb = 0
        self.vspeed = 0
        self.bpm = None
        self.date = None
        self.repetition = 0
        self.feeling = None

        self.where = None
        self.route = None
        self.notes = ""

        self.orig_json_string = ""

        # Distances split over basic running types
        self.basic_dist = {}
        self.basic_pace = {}
        self.basic_time = {}
        self.init_distribution_dictionaries()

        # List of segments
        self.structure = []

    def __eq__(self, other):
        if not isinstance(other, SingleRun):
            return False

        for (a, b) in zip(self.basic_dist.values(), other.basic_dist.values()):
            if not utilities.isclose(a, b, abs_tol=1e-3):
                return False

        for (a, b) in zip(self.basic_time.values(), other.basic_time.values()):
            if not utilities.isclose(a, b, abs_tol=1e-3):
                return False

        for (a, b) in zip(self.basic_pace.values(), other.basic_pace.values()):
            if not utilities.isclose(a, b, abs_tol=1e-3):
                return False

        # Compare structures
        if (len(self.structure) != len(other.structure)):
            return False

        for i in range(len(self.structure)):
            if self.structure[i] != other.structure[i]:
                return False

        if (self.pace is None and other.pace is not None) or\
            (self.pace is not None and self.pace is None):
            return False

        return self.type == other.type and\
            self.time == other.time and\
            utilities.isclose(self.distance, other.distance, abs_tol=1e-3) and\
            self.climb == other.climb and\
            utilities.isclose(self.pace, other.pace, abs_tol=1e-3) and\
            utilities.isclose(self.vspeed, other.vspeed, abs_tol=1e-3) and\
            self.date == other.date and\
            self.is_trail_running == other.is_trail_running and\
            self.where == other.where and\
            self.route == other.route and\
            self.feeling == other.feeling and\
            self.bpm == other.bpm and\
            self.notes == other.notes

    def __str__(self):
        str_ = []
        if self.date is not None:
            str_.append(f"Date: {self.date}")
        else:
            str_.append("Date: -")

        if self.where is not None:
            str_.append(f"Location: {self.where}")
        else:
            str_.append(f"Location: -")

        if self.route is not None:
            str_.append(f"Route: {self.route}")
        else:
            str_.append(f"Route: -")

        try:
            str_.append(f"Type: {types.RUN_TYPES_DICTIONARY[self.type]}")
        except KeyError:
            easy = types.RUN_TYPES_DICTIONARY[
                                types.BASIC_RUN_TYPES_ENUM.E]
            str_.append(f"Type: {easy}")

        if self.is_trail_running:
            str_.append("Trail running")

        if self.feeling is not None:
            str_.append(f"Feeling: {self.feeling}")
        else:
            str_.append(f"Feeling: -")

        try:
            str_.append("Total time: {:.0f}min".format(self.time))
        except TypeError:
            str_.append("Total time: -")

        try:
            str_.append("Total distance: {:0.2f}km".format(self.distance))
        except TypeError:
            str_.append("Total distance: -")

        str_.append("Climb: {:d}".format(self.climb))

        try:
            str_.append("Avg. pace: {:.0f} (in sec/km)".format(self.pace))
        except TypeError:
            str_.append("Avg. pace: -")

        str_.append("Avg. vert. speed:: {:.0f}".format(self.vspeed))

        str_.append("\nWith basic types:")
        str_.append("Stats by training speeds:")
        str_.append("=========================")

        b_type = types.BASIC_RUN_TYPES_DICTIONARY
        print_dist = {
            b_type[t]: d for (t, d) in self.basic_dist.items() if d != 0
        }
        str_.append(f"Distances (km): {print_dist}")

        print_time = {
            b_type[t]: tm for (t, tm) in self.basic_time.items() if tm != 0
        }
        str_.append(f"Times (sec): {print_time}")

        print_pace = {
            b_type[t]: p for (t, p) in self.basic_pace.items() if p != 0
        }
        str_.append(f"Paces (sec/km): {print_pace}")

        if len(self.structure) > 0:
            str_.append("\nStructure")
            str_.append("=====")
            for i, struct in enumerate(self.structure):
                str_.append(struct.__str__())
                if i != len(self.structure) - 1:
                    str_.append("")
            str_.append("=====")

        return "\n".join(str_)

    def as_dict(self):
        """ Converts segment into dictionary.
        This is later used to build a panda's DataFrame representation
        """
        E_ = types.BASIC_RUN_TYPES_ENUM.E
        M_ = types.BASIC_RUN_TYPES_ENUM.M
        T_ = types.BASIC_RUN_TYPES_ENUM.T
        I_ = types.BASIC_RUN_TYPES_ENUM.I
        R_ = types.BASIC_RUN_TYPES_ENUM.R
        X_ = types.BASIC_RUN_TYPES_ENUM.X
        XB_ = types.BASIC_RUN_TYPES_ENUM.XB

        rdict = {
            blockNames.Colnames.type: types.RUN_TYPES_DICTIONARY[self.type],
            blockNames.Colnames.time: self.time,
            blockNames.Colnames.distance: self.distance,
            blockNames.Colnames.climb: self.climb,
            blockNames.Colnames.avg_pace: self.pace,
            blockNames.Colnames.vspeed: self.vspeed,
            blockNames.Colnames.date: self.date,
            blockNames.Colnames.trail: self.is_trail_running,
            blockNames.Colnames.where: self.where,
            blockNames.Colnames.route: self.route,
            blockNames.Colnames.notes: self.notes,
            blockNames.Colnames.feeling: self.feeling,
            blockNames.Colnames.distE: self.basic_dist[E_],
            blockNames.Colnames.distM: self.basic_dist[M_],
            blockNames.Colnames.distT: self.basic_dist[T_],
            blockNames.Colnames.distI: self.basic_dist[I_],
            blockNames.Colnames.distR: self.basic_dist[R_],
            blockNames.Colnames.distX: self.basic_dist[X_],
            blockNames.Colnames.distXB: self.basic_dist[XB_],
            blockNames.Colnames.timeE: self.basic_time[E_],
            blockNames.Colnames.timeM: self.basic_time[M_],
            blockNames.Colnames.timeT: self.basic_time[T_],
            blockNames.Colnames.timeI: self.basic_time[I_],
            blockNames.Colnames.timeR: self.basic_time[R_],
            blockNames.Colnames.timeX: self.basic_time[X_],
            blockNames.Colnames.timeXB: self.basic_time[XB_],
            blockNames.Colnames.paceE: self.basic_pace[E_],
            blockNames.Colnames.paceM: self.basic_pace[M_],
            blockNames.Colnames.paceT: self.basic_pace[T_],
            blockNames.Colnames.paceI: self.basic_pace[I_],
            blockNames.Colnames.paceR: self.basic_pace[R_],
            blockNames.Colnames.paceX: self.basic_pace[X_],
            blockNames.Colnames.paceXB: self.basic_pace[XB_]
        }
        return rdict

    def get_structure_as_df(self):
        """ Returns a DataFrame from the list of segments

        Uses the segment.as_dict() function to build a pandas Series
        which is appended in a DataFrame

        Returns:
            DataFrame: DataFrame containing the structure
        """
        df = pd.DataFrame()
        for sgmnt in self.structure:
            ds_sgmnt = pd.Series(sgmnt.as_dict())
            df = df.append(ds_sgmnt, ignore_index=True)
        return df

    def load(self, parsed_json):
        """Loads the data in the input dictionary into the single run

        Loads the data in the input dictionary into the single run.
        The dicitonary *must* at least contain a time, distance and date.
        The rest of parameters are optional but further analysis can be
        performed when provided (e.g. segment analysis).

        When providing a running structure (with segments), different
        distances, times and paces are kept for each basic running type.
        These are assigned to the corresponding basic run type of each
        segment. If the segments' sum of distances and time do not add
        up to the total distance and time in the run, the difference is
        assigned to the easy pace, for consistency.

        Compulsory parameters:
            * Time
            * Distance
            * Date

        Optional parameters:
            * Type
            * Climb
            * Location (where)
            * Route
            * Trail
            * Feeling
            * Structure (running structure)

        Units:
            * distance: km
            * time: min
            * pace: sec/km
            * climb: m
            * vspeed: m/h

        Args:
            parsed_json (dict): Dictionary containing single run information

        Note:
            Dictionary keys are defined in constants.blockNames
        """

        self.orig_json_string = parsed_json

        parsed_json = dict((k.lower(), v) for k, v in parsed_json.items())

        # Compulsory, cannot be missing
        self.fill_time(parsed_json)
        self.fill_distance(parsed_json)
        self.fill_date(parsed_json)

        # Non compulsory
        self.fill_type(parsed_json)
        self.fill_climb(parsed_json)
        self.fill_where(parsed_json)
        self.fill_route(parsed_json)
        self.fill_is_trail_running(parsed_json)
        self.fill_feeling(parsed_json)
        self.fill_notes(parsed_json)

        # Fill run structure
        self.fill_structure(parsed_json)

        # Compute variables
        self.compute_vspeed()
        self.pace = self.compute_avg_pace()

        self.fill_basic_volume_dict_with_structure_volume()

        if not len(self.structure):
            self.fill_basic_volume_dict_with_guessed_type()

        self.fill_basic_volume_dict_with_unassigned_volume()
        self.compute_basic_pace_dictionary()

    def init_distribution_dictionaries(self):
        """Initializes distribution dictionaries

            Initializes distribution dictionaries (`basic_dist`,
            `basic_time`, and `basic_pace`). The first two are set
            to 0 and the latter to None.
        """
        for k in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            self.basic_dist[k] = 0
            self.basic_time[k] = 0
            self.basic_pace[k] = None

    def fill_time(self, config):
        """Fills time with data in input dictionary

            Fills time with the configuration dictionary.

            Args:
                config(dict): Dictionary with time information

            Notes:
                Time is a compulsory attribute
        """

        time_key = blockNames.FileParams.time
        try:
            time_str = config[time_key]
        except KeyError as err:
            error = f"Missing key: {time_key} in\n{config}"
            logging.exception(error)
            raise Exception(error) from err

        self.time = parser.parse_time(time_str)

    def fill_distance(self, config):
        """Fills distance with data in input dictionary

            Fills distance with the configuration dictionary.

            Args:
                config(dict): Dictionary with distance information

            Notes:
                Distance is a compulsory attribute
        """

        dist_key = blockNames.FileParams.distance
        try:
            distance_str = config[dist_key]
        except KeyError as err:
            error = f"Missing key: {dist_key} in\n{config}"
            logging.exception(error)
            raise Exception(error) from err

        self.distance = parser.parse_distance(distance_str)

    def fill_date(self, config):
        """Fills date with data in input dictionary

            Fills date with the configuration dictionary.

            Args:
                config(dict): Dictionary with date information

            Notes:
                Date is a compulsory attribute
        """

        date_key = blockNames.FileParams.date
        try:
            date_str = config[date_key]
        except KeyError as err:
            error = f"Missing key: {date_key} in\n{config}"
            logging.exception(error)
            raise Exception(error) from err

        self.date = parser.parse_date(date_str)

    def fill_type(self, config):
        """Fills type with data in input dictionary

            Fills type with the configuration dictionary. If the type
            is either not present in the dictionary, or it is a not supported
            one, it is set to types.RUN_TYPES_ENUM.E

            Args:
                config(dict): Dictionary with type information

            Notes:
                Supported activity types are defined in
                types.RUN_TYPES_DICTIONARY
        """
        try:
            type_str = config[blockNames.FileParams.type]
        except KeyError:
            type_str = types.RUN_TYPES_DICTIONARY[types.RUN_TYPES_ENUM.E]

        self.type = self.parse_type(type_str)

    def fill_climb(self, config):
        """Fills climb with data in input dictionary

            Fills climb with the configuration dictionary.
            If it is missing, climb is assigned to 0

            Args:
                config(dict): Dictionary with climb information
        """

        try:
            climb_str = config[blockNames.FileParams.climb]
        except KeyError:
            climb_str = 0

        self.climb = int(climb_str)

    def compute_vspeed(self):
        """Computes vertical speed

        Computes vertical speed. Needs of a time different to 0

        Units:
            meters/hour

        """

        try:
            self.vspeed = int(self.climb * 60. / self.time)
        except ZeroDivisionError:
            self.vspeed = float("NaN")

    def fill_where(self, config):
        """Fills location with data in input dictionary

            Fills location (where)  with the configuration dictionary.
            If it is missing, an empty string is assigned

            Args:
                config(dict): Dictionary with location information
        """

        try:
            where_str = config[blockNames.FileParams.where]
        except KeyError:
            where_str = ""

        self.where = where_str

    def fill_route(self, config):
        """Fills route with data in input dictionary

            Fills route with the configuration dictionary.
            If it is missing, an empty string is assigned

            Args:
                config(dict): Dictionary with route information
        """

        try:
            route_str = config[blockNames.FileParams.route]
        except KeyError:
            route_str = ""

        self.route = route_str

    def fill_is_trail_running(self, config):
        """Fills trail running flag  with data in input dictionary

            Fills trail running flag  with data in input dictionary
            It is set to the boolean evaluation of the input value
            If it is missing, trail running is assumed to be False

            Args:
                config(dict): Dictionary with trail running information
        """

        try:
            trail_str = config[blockNames.FileParams.trail]
        except KeyError:
            trail_str = False

        self.is_trail_running = bool(trail_str)

    def fill_feeling(self, config):
        """Fills feeling with data in input dictionary

            Fills feeling with the configuration dictionary.
            If it is missing, None value is assigned

            Args:
                config(dict): Dictionary with feeling information
        """

        try:
            feeling_str = config[blockNames.FileParams.feeling]
        except KeyError:
            feeling_str = None

        self.feeling = feeling_str

    def fill_notes(self, config):
        """Fills notes with data in input dictionary

            Fills notes with the configuration dictionary.
            If it is missing, an empty string is assigned

            Args:
                config(dict): Dictionary with notes data
        """

        try:
            notes_str = config[blockNames.FileParams.notes]
        except KeyError:
            notes_str = ""

        self.notes = notes_str

    def fill_structure(self, config):
        """Fills structure with data in input dictionary

            Fills structure with data in input dictionary

            Args:
                config(dict): Dictionary with structure data
        """

        try:
            struct_str = config[blockNames.FileParams.structure]
        except KeyError:
            struct_str = ""

        if struct_str:
            self.parse_structure(struct_str)

    def parse_structure(self, struct_list_dict):
        """Parses structure with data in the list of dictionaries

            Parses structure with data in the list of dictionaries.
            Data from the single run is passed into the segment, such as trail,
            feeling or date.
        """
        for rep_num, item in enumerate(struct_list_dict):
            sgmnt = segment.Segment()

            sgmnt.fill_segment(item)

            if not sgmnt.is_empty():
                sgmnt.repetition = rep_num
                sgmnt.is_trail_running = self.is_trail_running
                sgmnt.date = self.date
                sgmnt.feeling = self.feeling

                self.structure.append(sgmnt)

    def parse_type(self, type_str):
        """Parses type

            It parses the run type from the input argument. If not
            available, it is set to easy

            Args:
                type_str (str): string type

            Returns:
                int: run type in RUN_TYPES_DICTIONARY.
                If not found, returns types.RUN_TYPES.E

        """
        for (runType, runTypeBlockname) in types.RUN_TYPES_DICTIONARY.items():
            if type_str == runTypeBlockname:
                return runType

        logger = logging.getLogger()
        logging.warning(f"Assigning "\
            f"{types.RUN_TYPES_DICTIONARY[types.RUN_TYPES_ENUM.E]} type "\
            f"for run in {self.date}; {self.distance} km; {self.time} min ;"\
            f"with desc: {self.orig_json_string}")
        return types.RUN_TYPES_ENUM.E

    def fill_basic_volume_dict_with_structure_volume(self):
        """Fills basic dictionaries with structure.

            Fills basic_dist and basic_time dictionaries with structure data.
        """
        self.init_distribution_dictionaries()
        for sgmnt in self.structure:
            self.basic_dist[sgmnt.type] += sgmnt.distance
            if sgmnt.time is not None:
                self.basic_time[sgmnt.type] += sgmnt.time

    def fill_basic_volume_dict_with_guessed_type(self):
        """
            If the SingleRun type matches a Segment type,
            use that type to fill basic_time and basic_dist
            dictionaries.

            It requires self.type, self.distance and self.time
            to be set beforehand
        """
        dictkey = 0

        type_val = types.RUN_TYPES_DICTIONARY[self.type]
        if type_val in types.BASIC_RUN_TYPES_DICTIONARY.values():
            for (k1, v1) in types.BASIC_RUN_TYPES_DICTIONARY.items():
                if type_val == v1:
                    dictkey = k1
        else:
            dictkey = types.BASIC_RUN_TYPES_ENUM.E

        self.basic_dist[dictkey] = self.distance
        self.basic_time[dictkey] = self.time * 60
        self.basic_pace[dictkey] = self.time * 60 / self.distance

    def compute_avg_pace(self):
        """Computes the average pace of the single run

            Computes the average pace of the single run. Distance
            and time must have been set beforehand

            Time is assumed to be in minutes and distance in seconds.
            The avg. pace is stored in seconds/km
        """
        if self.time is not None and self.distance is not None:
            return self.time * 60 / self.distance
        else:
            return None

    def fill_basic_volume_dict_with_unassigned_volume(self):
        """Assigns the spare time and distance to a basic type.

            For consistency, the difference between the total distance
            and time is added into a distribution dictionary element,
            so that the sum over time and distance distribution
            dictionaries is equal to the total activity distance and
            time, respectively.

            If it is a running activity, it is assigned to the easy
            running type. If it is a cross training activity, it is
            assigned to the general activity type (e.g. X for an X
            activity).

            Note:

            This function assumes that basic_time and basic_distance
            dictionaries are filled with structured information.

            If no structure was used, the basic running type will be
            guessed.
        """

        str_type = types.RUN_TYPES_DICTIONARY[self.type]
        if str_type in types.RUNNING_ACTIVITIES:
            type_ = types.BASIC_RUN_TYPES_ENUM.E
        else:
            # Assign to cross training basic type
            for (k, v) in types.BASIC_RUN_TYPES_DICTIONARY.items():
                if str_type == v:
                    type_ = k

        assigned_dist = sum(self.basic_dist.values())
        self.basic_dist[type_] += self.distance - assigned_dist

        assigned_time = sum(self.basic_time.values())
        self.basic_time[type_] += self.time*60 - assigned_time

    def fill_basic_runtype_info_with_global_type(self):
        """
            Only applied when no structure was found

            It requires self.type, self.distance and self.time
            to be set beforehand
        """
        dictkey = 0

        type_val = types.RUN_TYPES_DICTIONARY[self.type]
        if type_val in types.BASIC_RUN_TYPES_DICTIONARY.values():
            for (k1, v1) in types.BASIC_RUN_TYPES_DICTIONARY.items():
                if type_val == v1:
                    dictkey = k1
        else:
            dictkey = types.BASIC_RUN_TYPES_ENUM.E

        self.basic_dist[dictkey] = self.distance
        self.basic_time[dictkey] = self.time * 60
        self.basic_pace[dictkey] = self.time * 60 / self.distance

    def compute_basic_pace_dictionary(self):
        """Computes the avg pace for each basic running type

            Computes the avg pace for each basic running type. If either
            time or distance is missing for a basic type, the basic pace
            is not computed
        """

        for t in types.BASIC_RUN_TYPES_DICTIONARY.keys():
            if self.basic_time[t] != 0 and self.basic_dist[t] != 0:
                self.basic_pace[t] = self.basic_time[t] / self.basic_dist[t]
