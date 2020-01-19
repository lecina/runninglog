import datetime
import re
import numbers
import sys

class Segment:
    def __init__(self):
        self.type = None
        self.distance = None
        self.time = None
        self.pace = None
        self.climb = 0
        self.bpm = None

        self.date = None

    def parse_date(self, date_str):
        fmt="%d/%m/%Y"
        try:
            dateObj = datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            fmt="%d/%m/%y"
            try:
                dateObj = datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                fmt="%d-%m-%Y"
                try:
                    dateObj = datetime.datetime.strptime(date_str, fmt)
                except ValueError:
                    fmt="%d-%m-%y"
                    try:
                        dateObj = datetime.datetime.strptime(date_str, fmt)
                    except ValueError:
                        sys.exit("Unknown date format")
        return dateObj.date()

    def parse_time(self, time_str):
        """
            Parses time and returns it in minutes
        """
        #solution based on https://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
        #work out regex a little bit more: only math r if h was matched
        regex = re.compile(r'((?P<hours>\d+?)h)?([r])?((?P<minutes>\d+?)m)?([i])?([n])?((?P<seconds>\d+?)s)?')
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

    def parse_distance(self, dist_str):
        """
            Parses distance and returns it in km
        """
        if isinstance(dist_str, numbers.Number):
            return dist_str #not actually a string

        regex = re.compile(r'((?P<km>\d(.\d+)?))?')
        dist = regex.search(dist_str).groupdict()

        return float(dist["km"])
    
    def parse_pace(self, pace_str):
        if pace_str is None:
            return None

        if isinstance(pace_str, numbers.Number):
            return pace_str #not a string

        regex = re.compile(r'((?P<min>\d):(?P<sec>\d+?))$')
        pace_dict = regex.search(pace_str).groupdict()

        pace = int(pace_dict["min"])*60 + int(pace_dict["sec"])

        return pace


    def create_segment(self, segment_dict):
        #Type and distance are compulsory
        item_dict = dict((k.lower(), v) for k, v in segment_dict.iteritems())

        parsed_type = item_dict[blockNames.FileParams.type]
        if parsed_type in runTypes.BASIC_RUN_TYPES_DICTIONARY.values():
            self.type = parsed_type
        else:
            sys.exit("Unknown run type in segment: %s", key)

        #distance is compulsory
        self.distance = self.parse_distance(item_dict[blockNames.FileParams.distance])

        #date is passed
        try:
            self.date = self.parse_date(item_dict[blockNames.FileParams.date])
        except KeyError:
            pass

        try:
            self.climb = item_dict[blockNames.FileParams.climb]
        except KeyError:
            pass

        try:
            self.bpm = item_dict[blockNames.FileParams.bpm]
        except KeyError:
            pass

        #When only pace or time are given, the other one is guessed
        #When both are given, pace is used to compute the time in order
        #to ensure consistency
        #If none is given, then do nothing
        try:
            pace_str = item_dict[blockNames.FileParams.pace]
        except KeyError:
            pace_str = None

        try:
            time_str = item_dict[blockNames.FileParams.time]
        except KeyError:
            time_str = None

        if pace_str is not None:
            parsed_pace = self.parse_pace(pace_str)
            self.time = self.distance * parsed_pace
        elif time_str is not None:
            parsed_time = self.parse_time(time_str) * 60
            parsed_pace = parsed_time / self.distance
        else:
            parsed_time = None
            parsed_pace = None
