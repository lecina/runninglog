import pandas as pd

from runninglog.run import types

def agg_df(df, time_option):
    """Aggregate df by date, activity, and trail indicator

        Aggregate df, groupping by date, activity, and trail indicator

        Args:
            df(DataFrame): DataFrame to aggregate
            time_option(str): time option (week, month, year, all)
    """
    if time_option == 'week':
        agg_option = 'W'
    elif time_option == 'month':
        agg_option = 'MS'
    elif time_option == 'year':
        agg_option = 'YS'
    elif time_option == 'all':
        agg_option = '2Y'
    else:
        error = f"Unknown aggregation {time_option}"
        raise Exception(error)

    # Cols to be summed in agg
    sum_cols = ['distance', 'time', 'climb']
    dcols = ['dist%s'%v for v in types.BASIC_RUN_TYPES_DICTIONARY.values()]
    sum_cols.extend(dcols)
    tcols = ['time%s'%v for v in types.BASIC_RUN_TYPES_DICTIONARY.values()]
    sum_cols.extend(tcols)

    # Cols to be averaged in agg
    avg_cols = ['feeling']

    dict_sum = {i: 'sum' for i in sum_cols}
    dict_avg = {i: 'mean' for i in avg_cols}
    dict_count = {'date': 'size'}
    desc_dict = {**dict_sum, **dict_avg, **dict_count}

    df_agg = df.groupby(['activity', 'trail'])\
                    .resample(agg_option, on='date')\
                    .agg(desc_dict)\
                    .rename(columns={'date': 'N'})

    df_agg.reset_index(level=0, inplace=True)

    df_agg.sort_values(by=['date', 'activity', 'trail'], inplace=True)

    return df_agg

def agg_by_date(df, chosen_activities, trail_road_selector, time_option=''):
    """Filter and Aggregate df by date

        Filter and Aggregate groupping by date, activity, and trail indicator

        Args:
            df(DataFrame): DataFrame to aggregate
            chosen_activities(list): list of activities to consider
            trail_road_selector(list): selection_list
            time_option(str): time option (week, month, year, all)
    """
    #df.reset_index(inplace=True)

    #chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
    #filt_df = df[df.activity.isin(chosen_activity_types)]
    filt_df = df[df.activity.isin(chosen_activities)]

    #trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
    trail_road = trail_road_selector
    filt_df = filt_df[filt_df.trail.isin(trail_road)]

    # If nothing matches, return empty DataFrame
    if filt_df.shape[0] == 0:
        cols = [
            'date',
            'distance',
            'time',
            'climb',
            'distE', 'distM', 'distT', 'distI', 'distR', 'distX', 'distXB',
            'timeE', 'timeM', 'timeT', 'timeI', 'timeR', 'timeX', 'timeXB',
            'feeling',
            'N', 'n_trail', 'n_road',
            'distance_trail', 'distance_road',
            'Nall_Nroad_Ntrail',
            '%E', '%M', '%T', '%I', '%R', '%X', '%XB', '%types'
        ]
        data = [0]*len(cols)
        #return pd.DataFrame(columns = cols, data = [data]).\
        #                        to_json(date_format='iso', orient='split')
        return pd.DataFrame(columns = cols, data = [data])

    #END apply filters

    # New cols
    filt_df.feeling = filt_df.feeling * filt_df.N
    filt_df['N_feeling'] = (1 - pd.isnull(filt_df.feeling)) * filt_df.N
    filt_df['n_trail'] = filt_df.trail * filt_df.N
    filt_df['n_road'] = (1 - filt_df.trail) * filt_df.N
    filt_df['distance_trail'] = filt_df.trail * filt_df.distance
    filt_df['distance_road'] = (1 - filt_df.trail) * filt_df.distance

    # Cols to be summed in agg
    sum_cols = [
                'distance',
                'time',
                'climb',
                'feeling',
                'N_feeling',
                'N',
                'n_trail',
                'n_road',
                'distance_trail',
                'distance_road'
               ]
    dcols = ['dist%s'%v for v in types.BASIC_RUN_TYPES_DICTIONARY.values()]
    sum_cols.extend(dcols)
    tcols = ['time%s'%v for v in types.BASIC_RUN_TYPES_DICTIONARY.values()]
    sum_cols.extend(tcols)

    df_agg = filt_df.groupby(['date'])\
                    .agg({i: 'sum' for i in sum_cols})\
                    .rename(columns={'date': 'N'})

    df_agg.feeling = df_agg.feeling / df_agg.N_feeling
    df_agg.drop('N_feeling', axis=1, inplace=True)

    df_agg.reset_index(level=0, inplace=True)

    df_agg.sort_values(by=['date'], inplace=True)

    cols = ['n_road', 'n_trail', 'N']
    df_agg['Nall_Nroad_Ntrail'] = df_agg[cols].apply(
            lambda row: "%d/%.0f/%.0f" % (row.values[2],
                                          row.values[0],
                                          row.values[1]),
                                        axis=1)


    #df_agg[time_option] = df_agg.index

    pattern = '%Y-%m-%d'
    df_agg['date'] = df_agg['date'].apply(lambda x: x.strftime(pattern))

    tot_sum =   df_agg['distE'] +\
                df_agg['distI'] +\
                df_agg['distM'] +\
                df_agg['distR'] +\
                df_agg['distT']

    df_agg['%E'] = 100*df_agg['distE'] / tot_sum
    df_agg['%M'] = 100*df_agg['distM'] / tot_sum
    df_agg['%T'] = 100*df_agg['distT'] / tot_sum
    df_agg['%I'] = 100*df_agg['distI'] / tot_sum
    df_agg['%R'] = 100*df_agg['distR'] / tot_sum
    df_agg['%X'] = df_agg['%XB'] = 0

    df_agg.fillna(value={'%E':0, '%M':0, '%T':0, '%I':0, '%R':0}, inplace=True)

    cols = ['%E','%M','%T','%I','%R']
    df_agg['%types'] = df_agg[cols].apply(lambda row:
"%.0f(%.0f)%%/%.0f%%/%.0f%%/%.0f%%"%(row.values[0]+row.values[1],row.values[1],row.values[2],row.values[3],row.values[4]),
axis=1)

    decimals = pd.Series([1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0], index=['distance',
'time', 'climb', 'run_avg_pace', '%E', '%M', '%T', '%I', '%R', 'feeling',
'vspeed'])

    return df_agg.round(decimals)
    #return df_agg.round(decimals).to_json(date_format='iso', orient='split')

