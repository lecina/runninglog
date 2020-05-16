from runninglog.constants import blockNames
from runninglog.run import types
from runninglog.io import parser
from runninglog.utilities import utilities


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
            type_ = types.BASIC_RUN_TYPES_DICTIONARY[self.type]
            str_.append(f"Type: {type_}")

        if self.is_trail_running:
            str_.append("Trail running segment")

        try:
            str_.append(f"Feeling: {self.feeling}")
        except TypeError:
            str_.append(f"Feeling: -")

        try:
            str_.append("Time: {:.0f}sec".format(self.time))
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
        str_.append("Vert. speed: {:.0f}".format(self.vspeed))

        return "; ".join(str_)

    def __eq__(self, other):
        return isinstance(other, Segment) and\
            self.type == other.type and\
            self.is_trail_running == other.is_trail_running and\
            utilities.isclose(self.distance, other.distance, abs_tol=1e-3) and\
            self.time == other.time and\
            utilities.isclose(self.pace, other.pace, abs_tol=1e-3) and\
            self.climb == other.climb and\
            utilities.isclose(self.vspeed, other.vspeed, abs_tol=1e-3) and\
            self.bpm == other.bpm and\
            self.date == other.date and\
            self.repetition == other.repetition and\
            self.feeling == other.feeling

    def as_dict(self):
        """ Converts segment into dictionary.
        This is later used to build a panda's DataFrame representation
        """
        type_ = types.BASIC_RUN_TYPES_DICTIONARY[self.type]
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

        parsed_type = parser.parse_type(type_)

        if parsed_type is not None:
            self.type = parsed_type
        else:
            error = f"Unknown type in segment: {item_dict}"
            raise ValueError(error)

        # Distance
        str_distance = item_dict[blockNames.FileParams.distance]
        self.distance = parser.parse_distance(str_distance)

        # Date
        try:
            self.date = parser.parse_date(item_dict[blockNames.FileParams.date])
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
            self.pace = parser.parse_pace(pace_str)
            self.time = self.distance * self.pace
        elif time_str is not None:
            self.time = parser.parse_time(time_str) * 60
            self.pace = self.time / self.distance
        else:
            parsed_time = None
            parsed_pace = None

        if self.time is not None:
            self.vspeed = int(self.climb * 3600. / self.time)  # vspeed in m/h
