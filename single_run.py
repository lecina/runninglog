import blockNames
import datetime
import re
import numbers
import runTypes

class SingleRun:
    def __init__(self):
        self.type = ""

        self.total_time = 0 #min
        self.total_distance = 0 #km
        self.climb = 0 #m

        self.avg_pace = None #sec

        self.date = None
        self.where = None

        self.dist = {}
        self.dist["E"] = 0
        self.dist["M"] = 0
        self.dist["T"] = 0
        self.dist["I"] = 0
        self.dist["R"] = 0
        self.dist["WU"] = 0
        self.dist["CD"] = 0

        self.pace = {}
        self.pace["E"] = 0
        self.pace["M"] = 0
        self.pace["T"] = 0
        self.pace["I"] = 0
        self.pace["R"] = 0
        self.pace["WU"] = 0
        self.pace["CD"] = 0
        

    def load_json(self, parsed_json):
        #Make some of them optional? date? struct?
        self.type = self.parse_type(parsed_json[blockNames.FileParams.type])
        self.date = self.parse_date(parsed_json[blockNames.FileParams.date])
        self.total_time = self.parse_total_time(parsed_json[blockNames.FileParams.time])
        self.total_distance = self.parse_total_distance(parsed_json[blockNames.FileParams.distance])
        self.struct = self.parse_struct(parsed_json[blockNames.FileParams.structure])

        #compute other measures
        self.avg_pace = self.compute_avg_pace()

    def compute_avg_pace(self):
        if self.total_time is not None and self.total_distance is not None:
            return self.total_time * 60 / self.total_distance
        else:
            return None

    def parse_type(self, type_str):
        if type_str in runTypes.RUN_TYPES_DICTIONARY.values():
            return type_str
        else:
            return blockNames.RunTypes.E

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
                        print "Unknown date format"
        return dateObj

    def parse_total_time(self, time_str):
        """
            Parses time and returns it in minutes
        """
        #solution based on https://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
        #work out regex a little bit more
        regex = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
        time = regex.search(time_str).groupdict()

        time_in_minutes = 0
        if time["hours"] is not None: 
            time_in_minutes += int(time["hours"]) * 60 
        if time["minutes"] is not None: 
            time_in_minutes += int(time["minutes"])
        if time["seconds"] is not None: 
            time_in_minutes += float(time["seconds"])/60

        return time_in_minutes

    def parse_total_distance(self, dist_str):
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

    def parse_struct(self, struct_str):
        #TODO: protect
        keys = struct_str.keys()

        for key,val in struct_str.iteritems():
            if key in runTypes.BASIC_RUN_TYPES_DICTIONARY.values():
                self.dist[key] = self.parse_total_distance(val[blockNames.FileParams.distance])
                try:
                    pace_str = val[blockNames.FileParams.pace]
                except KeyError:
                    pace_str = None

                self.pace[key] = self.parse_pace(pace_str)

            else:
                sys.exit("Unknown sub-run type: %s", key)

        return struct_str
