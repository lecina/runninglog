import datetime
import re
import numbers
import sys

from runninglog.constants import blockNames
from runninglog.single_run import runTypes


class Segment:
    """Basic run element of a given type.
    It must have a type and a distance. The rest of parameters are optional
    A single run may contain from none to an indefinite number of them.

    Units:
        distance: km
        time: sec
        climb: m
        pace: sec/km
        vspeed: m/h
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

    def __str__(self):
        str_ = []
        if self.date is not None:
            str_.append(f"Date: {self.date}")
        else:
            str_.append("Date: -")

        str_.append(f"Repetition: {self.repetition}")

        if self.type is None:
            str_.append("Type: not yet defined")
        else:
            type_ = runTypes.BASIC_RUN_TYPES_DICTIONARY[self.type]
            str_.append(f"Type: {type_}")

        if self.is_trail_running:
            str_.append("Trail running segment")

        try:
            str_.append(f"Feeling: {self.feeling}")
        except TypeError:
            str_.append(f"Feeling: -")

        try:
            str_.append("Time: {:.0f}min".format(self.time))
        except TypeError:
            str_.append("Total time: -")

        try:
            str_.append("Distance: {:0.2f}km".format(self.distance))
        except TypeError:
            str_.append("Distance: -")

        str_.append("Climb: {:d}".format(self.climb))

        try:
            str_.append("Pace: {:.0f} (in sec/km)".format(self.pace))
        except TypeError:
            str_.append("Pace: -")
        str_.append("Vert. speed:: {:.0f}".format(self.vspeed))

        return "\n".join(str_)

    def as_dict(self):
        """ Converts segment into dictionary.
        This is later used to build a panda's DataFrame representation
        """
        type_ = runTypes.BASIC_RUN_TYPES_DICTIONARY[self.type]
        rdict = {
            blockNames.Colnames.type: type_,
            blockNames.Colnames.trail: self.is_trail_running,
            blockNames.Colnames.feeling: self.feeling,
            blockNames.Colnames.time: self.time,
            blockNames.Colnames.distance: self.distance,
            blockNames.Colnames.avg_pace: self.pace,
            blockNames.Colnames.climb: self.climb,
            blockNames.Colnames.bpm: self.bpm,
            blockNames.Colnames.date: self.date,
            blockNames.Colnames.repetition: self.repetition
        }
        return rdict

    def is_empty(self):
        """
        Checks if segment is empty
        """
        return (self.type is None and
                self.is_trail_running is False and
                self.distance == 0 and
                self.time is None and
                self.pace is None and
                self.climb == 0 and
                self.vspeed == 0 and
                self.bpm is None and
                self.feeling == None and
                self.repetition == 0)

    def fill_segment(self, segment_dict):
        """Fills the segment with the data in the dictionary

        Fills the segment with the data in the input dictionary.
        A segment type and a distance must be provided. The rest of
        parameters are optional but further analysis can be performed
        when provided (e.g. pace analysis or vspeed analysis).

        When one of pace or time are given, the other one is computed
        When both are given, pace is used to compute the time in order
        to enseure consistency. As expected, if none are given, they
        are left unfilled


        Units:
            distance: km
            time: sec
            climb: m
            pace: sec/km
            vspeed: m/h

        Args:
            segment_dict (dict): Dictionary containing segment information

        Note:
            Dictionary keys are defined in constants.blockNames
        """
        item_dict = dict((k.lower(), v) for k, v in segment_dict.items())

        # If empty, return empty segment
        if item_dict == {}:
            return

        # Parsing compulsory elements
        # Type
        type_key = blockNames.FileParams.type
        try:
            type_ = item_dict[type_key]
        except KeyError as err:
            raise Exception(f"Missing key: {type_key} in\n{item_dict}") from err

        parsed_type = self.parse_type(type_)

        if parsed_type is not None:
            self.type = parsed_type
        else:
            error = f"Unknown type in segment: {item_dict}"
            raise ValueError(error)

        # Distance
        str_distance = item_dict[blockNames.FileParams.distance]
        self.distance = self.parse_distance(str_distance)

        # Date
        try:
            self.date = self.parse_date(item_dict[blockNames.FileParams.date])
        except KeyError:
            pass

        # Repetition
        try:
            self.repetition = item_dict[blockNames.FileParams.rep]
        except KeyError:
            try:
                self.repetition = item_dict[blockNames.FileParams.rep_alt]
            except KeyError:
                pass

        # Climb
        try:
            self.climb = item_dict[blockNames.FileParams.climb]
        except KeyError:
            pass

        # BPM
        try:
            self.bpm = item_dict[blockNames.FileParams.bpm]
        except KeyError:
            pass

        # Pace and time.
        # If one is given, the other is computed.
        # If both are given, pace is used to compute time for consistency
        try:
            pace_str = item_dict[blockNames.FileParams.pace]
        except KeyError:
            pace_str = None

        try:
            time_str = item_dict[blockNames.FileParams.time]
        except KeyError:
            time_str = None

        if pace_str is not None:
            self.pace = self.parse_pace(pace_str)
            self.time = self.distance * self.pace
        elif time_str is not None:
            self.time = self.parse_time(time_str) * 60
            self.pace = self.time / self.distance
        else:
            parsed_time = None
            parsed_pace = None

        if self.time is not None:
            self.vspeed = int(self.climb * 3600. / self.time)  # vspeed in m/h

    def parse_type(self, type_str):
        """Parses type

            It parses the segment type from the input argument

            Args:
                type_str (str): string type

            Returns:
                int: run type in BASIC_RUN_TYPES_DICTIONARY.
                If not found, returns None

        """
        for (runType, runTypeBlockname) in\
                runTypes.BASIC_RUN_TYPES_DICTIONARY.items():
            if type_str == runTypeBlockname:
                return runType

        return None

    def parse_date(self, date_str):
        fmt = "%d/%m/%Y"
        try:
            dateObj = datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            fmt = "%d/%m/%y"
            try:
                dateObj = datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                fmt = "%d-%m-%Y"
                try:
                    dateObj = datetime.datetime.strptime(date_str, fmt)
                except ValueError:
                    fmt = "%d-%m-%y"
                    try:
                        dateObj = datetime.datetime.strptime(date_str, fmt)
                    except ValueError:
                        sys.exit("Unknown date format")
        return dateObj.date()

    def parse_time(self, time_str):
        """Parses time

            It parses the segment time from the input argument pace and
            returns it in minutes

            Args:
                time_str (str): string with XXh XXmin XXsec format

            Returns:
                int: time in minutes

            Note:
                The hour can be written as: 'h' or 'hr'
                The minutes can be written as: 'min', 'mi', 'mn' or 'm'
                Seconds can be written as: 's'
        """
        regex = re.compile(r'((?P<hours>\d+?)hr?)?'
                           r'((?P<minutes>\d+?)m)?([i])?([n])?'
                           r'((?P<seconds>\d+?)s)?')
        time_str = time_str.replace(" ", "")
        time = regex.search(time_str).groupdict()

        time_in_minutes = 0
        if time["hours"] is not None:
            time_in_minutes += int(time["hours"]) * 60
        if time["minutes"] is not None:
            time_in_minutes += int(time["minutes"])
        if time["seconds"] is not None:
            time_in_minutes += float(time["seconds"])/60

        return time_in_minutes

    def parse_distance(self, dist):
        """Parses distance

            It parses the segment distance from the input argument in dist
            Distance must be given in km

            Args:
                dist (int or str): distance in int or str format

            Returns:
                int: pace in seconds/km

            Note:
                Only the numerical part is extracted
                Hence 10km is interpreted in the same way as 10m
        """
        # If it is a number, do not preprocess
        if isinstance(dist, numbers.Number):
            return dist

        regex = re.compile(r'((?P<km>\d+(.\d+)?))?')
        distance = regex.search(dist).groupdict()

        return float(distance["km"])

    def parse_pace(self, pace):
        """Parses pace

            It parses the segment pace from the input argument pace

            Args:
                pace (int or str): If pace is an integer, it is supposed
                    to be in seconds/km. If it is a string it is supposed
                    to be in minutes:seconds/km
            Returns:
                int: pace in seconds/km
        """
        if pace is None:
            return None

        # If it is a number, do not preprocess
        if isinstance(pace, numbers.Number):
            return pace

        regex = re.compile(r'((?P<min>\d+):(?P<sec>\d+?))$')
        pace_dict = regex.search(pace).groupdict()

        parsed_pace = int(pace_dict["min"])*60 + int(pace_dict["sec"])

        return parsed_pace
