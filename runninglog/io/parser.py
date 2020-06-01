import datetime
import re
import numbers
import logging

from runninglog.run import types
from runninglog.constants import blockNames

def parse_activity(activity_str):
    """Parses activity

        It parses the activity type from the input argument

        Args:
            type_str (str): Activity as string

        Returns:
            type.ACTIVITIES: Activity type
            If not found, returns None

    """
    for activity in blockNames.Activities.available_activities:
        if activity_str.lower() == activity.lower():
            return activity
    return None

def parse_type(type_str):
    """Parses type

        It parses the segment type from the input argument

        Args:
            type_str (str): string type

        Returns:
            int: run type in BASIC_RUN_TYPES_DICTIONARY.
            If not found, returns None

    """
    for (runType, runTypeBlockname) in\
            types.BASIC_RUN_TYPES_DICTIONARY.items():
        if type_str == runTypeBlockname:
            return runType

    return None

def parse_date(date_str):
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
                except ValueError as er:
                    logging.exception(f"Unknown date format:{date_str}")
                    raise Exception(f"Unknown date format:{date_str}") from er
    return dateObj.date()

def parse_time(time_str):
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

def parse_distance(dist):
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

def parse_pace(pace):
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
