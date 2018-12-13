import blockNames
import datetime
import re
import numbers
import runTypes
import sys

class SingleRun:
    def __init__(self):
        self.type = ""

        self.total_time = 0 #min
        self.total_distance = 0 #km
        self.climb = 0 #m

        self.avg_pace = None #sec

        self.date = None
        self.where = None

        self.notes = ""

        #distances split over basic running types
        self.basic_dist = {}
        self.basic_pace = {}
        for k in runTypes.BASIC_RUN_TYPES_DICTIONARY.iterkeys():
            self.basic_dist[k] = 0 
            self.basic_pace[k] = None

    def __str__(self):
        str_to_return = ""
        if self.date is not None:
            str_to_return += "Date: %s\n"%self.date.date()
        if self.where is not None:
            str_to_return += "Location: %s\n"%self.where

        str_to_return += "Type: %s\n"%runTypes.RUN_TYPES_DICTIONARY[self.type]

        str_to_return += "Total time: %dmin\n"%self.total_time
        str_to_return += "Total distance: %.2fkm\n"%self.total_distance
        str_to_return += "\nTotal climb: %d\n"%self.climb

        str_to_return += "Avg pace: %d (in sec/km)\n"%self.avg_pace

        str_to_return += "\nWith basic types:"
        str_to_return += "\nStats by training speeds:"
        str_to_return += "\n=========================\n"

        print_dist = {}
        for (t, d) in self.basic_dist.iteritems():
            if d != 0:
                blockname_type = runTypes.BASIC_RUN_TYPES_DICTIONARY[t]
                print_dist[blockname_type] = d
        str_to_return += "Distances (km): %s\n"%print_dist

        print_pace = {}
        for (t, p) in self.basic_pace.iteritems():
            if p is not None: 
                blockname_type = runTypes.BASIC_RUN_TYPES_DICTIONARY[t]
                print_pace[blockname_type] = p
        str_to_return += "Paces (sec/km): %s\n"%print_pace

        return str_to_return

    def load_json(self, parsed_json):
        parsed_json = dict((k.lower(), v) for k, v in parsed_json.iteritems())

        #Compulsory
        self.total_time = self.parse_total_time(parsed_json[blockNames.FileParams.time])
        #Compulsory
        self.total_distance = self.parse_distance(parsed_json[blockNames.FileParams.distance])
        #Compulsory
        self.date = self.parse_date(parsed_json[blockNames.FileParams.date])


        #type
        try:
            type_str = parsed_json[blockNames.FileParams.type]
        except KeyError:
            type_str = ""

        if type_str != "":
            self.type = self.parse_type(type_str)
        else:
            self.type = runTypes.RUN_TYPES.E

        #climb
        try:
            climb_str = parsed_json[blockNames.FileParams.climb]
        except KeyError:
            climb_str = ""

        if climb_str != "":
            self.climb = int(climb_str)  
        else:
            self.climb = 0 

        #where
        try:
            where_str = parsed_json[blockNames.FileParams.where]
        except KeyError:
            where_str = ""
        self.where = where_str

        #struct
        try:
            struct_str = parsed_json[blockNames.FileParams.structure]
        except KeyError:
            struct_str = ""

        if struct_str != "":
            self.fill_basic_runtype_info_with_dict(struct_str)
        else:
            self.fill_basic_runtype_info_with_global_type()


        #notes
        try:
            self.notes = parsed_json[blockNames.FileParams.notes]
        except KeyError:
            pass

        #compute other measures
        self.avg_pace = self.compute_avg_pace()
        self.redistribute_distances()


    def parse_type(self, type_str):
        """
            Parses run type. If not found, set it to E.
        """
        for (runType, runTypeBlockname) in runTypes.RUN_TYPES_DICTIONARY.iteritems():
            if type_str == runTypeBlockname:
                return runType

        #If run_type is not found, set it to E
        return runTypes.RUN_TYPES.E

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
        return dateObj

    def parse_total_time(self, time_str):
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

    def fill_basic_runtype_info_with_dict(self, struct_dict):
        for key,val in struct_dict.iteritems():
            val = dict((k.lower(), v) for k, v in val.iteritems())
            if key in runTypes.BASIC_RUN_TYPES_DICTIONARY.values():
                dictkey = 0
                for (k1,v1) in runTypes.BASIC_RUN_TYPES_DICTIONARY.iteritems():
                    if key==v1: dictkey = k1

                #distance is compulsory
                self.basic_dist[dictkey] = self.parse_distance(val[blockNames.FileParams.distance])
                try:
                    pace_str = val[blockNames.FileParams.pace]
                except KeyError:
                    pace_str = None

                self.basic_pace[dictkey] = self.parse_pace(pace_str)

            else:
                sys.exit("Unknown sub-run type: %s", key)

    def fill_basic_runtype_info_with_global_type(self):
        """
            Only applied when no structure was found

            It requires self.type, self.total_distance and self.total_time
            to be set beforehand
        """
        dictkey = 0
        if self.type in runTypes.BASIC_RUN_TYPES_DICTIONARY.values():
            for (k1,v1) in runTypes.BASIC_RUN_TYPES_DICTIONARY.iteritems():
                if key==v1: 
                    dictkey = k1
            self.basic_dist[dictkey] = self.total_distance
        else:
            dictkey = runTypes.BASIC_RUN_TYPES.E

        self.basic_dist[dictkey] = self.total_distance
        self.basic_pace[dictkey] = self.total_time * 60 / self.total_distance

    def compute_avg_pace(self):
        if self.total_time is not None and self.total_distance is not None:
            return self.total_time * 60 / self.total_distance
        else:
            return None

    def redistribute_distances(self):
        #grouping into basic run types 
        self.basic_dist[runTypes.BASIC_RUN_TYPES.E] += self.basic_dist[runTypes.BASIC_RUN_TYPES.WU]
        self.basic_dist[runTypes.BASIC_RUN_TYPES.E] += self.basic_dist[runTypes.BASIC_RUN_TYPES.CD]
        #TODO: add as different running type?
        #self.basic_dist[runTypes.BASIC_RUN_TYPES.E] += self.basic_dist[runTypes.RUN_TYPES.X] 

        self.basic_dist[runTypes.BASIC_RUN_TYPES.WU] = 0
        self.basic_dist[runTypes.BASIC_RUN_TYPES.CD] = 0

        #to account for innacuracies, e.g due to jogging in between intervals
        self.basic_dist[runTypes.BASIC_RUN_TYPES.E] += self.total_distance - sum(self.basic_dist.values())
