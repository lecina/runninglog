import numpy as np

from runninglog.constants import blockNames
from runninglog.run import types

def get_runType_colors():
    runType_colors = {  
                blockNames.RunTypes.E:'#1f77b4', # muted blue
                blockNames.RunTypes.M:'#ff7f0e', # safety orange
                blockNames.RunTypes.T:'#2ca02c', # cooked asparagus green
                blockNames.RunTypes.I:'#d62728', # brick red
                blockNames.RunTypes.R:'#9467bd', # muted purple
                blockNames.RunTypes.C:'#17becf', # blue-teal
                blockNames.RunTypes.X:'#8c564b', # chestnut brown
                blockNames.RunTypes.XB:'#bb6600'}
    return runType_colors

def get_runType_order():
    runType_order = [blockNames.RunTypes.E, 
                     blockNames.RunTypes.M,
                     blockNames.RunTypes.T,
                     blockNames.RunTypes.I,
                     blockNames.RunTypes.R,
                     blockNames.RunTypes.C,
                     blockNames.RunTypes.X,
                     blockNames.RunTypes.XB]
    return runType_order


def get_year_marks(df):
    #years = df.date.dt.year
    #year_marks={year: {'label':str(year), 'style':{'font-size':'1.2em'}} for year in np.hstack([years.unique(), [years.max()+1], [years.max()+2]])}
    #year_marks[years.max()+1] = {'label':'Last year', 'style':{'font-size':'1.2em'}}
    #year_marks[years.max()+2] = {'label':'All', 'style':{'font-size':'1.2em'}}

    years = list(set(df.date.dt.year.tolist()))
    max_year = max(years)

    year_marks={year: {'label':str(year), 'style':{'font-size':'1.2em'}} for year in years + [max_year+1, max_year+2]}
    year_marks[max_year+1] = {'label':'Last year', 'style':{'font-size':'1.2em'}}
    year_marks[max_year+2] = {'label':'All', 'style':{'font-size':'1.2em'}}

    return year_marks

def get_activities_from_checklist(chosen_activity_types):
    chosen_types = []
    if 'Running' in chosen_activity_types:
        chosen_types = types.RUNNING_ACTIVITIES[:]
    if 'X' in chosen_activity_types:
        chosen_types.append(blockNames.RunTypes.X)
    if 'XB' in chosen_activity_types:
        chosen_types.append(blockNames.RunTypes.XB)

    if chosen_types == []:
        chosen_types = types.RUNNING_ACTIVITIES[:]

    return chosen_types

def get_trail_road_activities(trail_road_selector):
    if trail_road_selector == 'Trail':
        return [1]
    elif trail_road_selector == 'Road':
        return [0]
    elif trail_road_selector == 'All':
        return [0, 1]
