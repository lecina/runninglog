import blockNames
import datetime
import re
import numbers

class SingleRun:
    def __init__(self):
        self.type = ""

        self.total_time = 0 #min
        self.total_distance = 0 #km

        self.date = "" #change for actual date

        self.dist_E = 0
        self.dist_M = 0
        self.dist_T = 0
        self.dist_I = 0
        self.dist_R = 0

        self.climb = 0 #m
        
        self.avg_pace = 0 #sec

    def load_json(self, parsed_json):
        self.type = parsed_json[blockNames.FileParams.type]
        self.date = self.parse_date(parsed_json[blockNames.FileParams.date])
        self.total_time = self.parse_total_time(parsed_json[blockNames.FileParams.time])
        self.total_distance = self.parse_total_distance(parsed_json[blockNames.FileParams.distance])
        struct = parsed_json[blockNames.FileParams.structure]

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
