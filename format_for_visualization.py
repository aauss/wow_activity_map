import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from copy import deepcopy

cleaned_server_activity = pickle.load(open('cleaned_server_activity.p', 'rb'))

time_shift = {'America/Chicago': -5,
              'America/Denver': -7,
              'America/Los_Angeles': -8,
              'America/New_York': -4,
              'America/Sao_Paulo': -3,
              'Australia/Melbourne': 10,
              'de_DE': 1,
              'fr_FR': 1,
              'en_GB': 0,
              'es_ES': 1,
              'it_IT': 1,
              'pt_PT': 0,
              'ru_RU': 3}


def format_for_visualization(cleaned_server_activity, local_entity, continent_abb):
    # Format the crawled server activity such that it can be visualized

    blizz_realms = pickle.load(open('blizz_realms_{}.p'.format(continent_abb), 'rb'))['realms']  # From Blizzard API
    blizz_realms_and_timezone = [(blizz_realms[i]['name'], blizz_realms[i][local_entity])
                                 for i in range(len(list(blizz_realms)))]
    blizz_realms_and_timezone = pd.DataFrame(blizz_realms_and_timezone, columns=['server_name', local_entity])
    timezone_dict = blizz_realms_and_timezone.groupby(local_entity).groups

    # Create a dict with timezone as key and server names as values (instead of index)
    timezone_dict_to_convert = deepcopy(timezone_dict)
    timezone_dict = {}
    for key in timezone_dict_to_convert.keys():
        timezone_dict[key] = blizz_realms_and_timezone.iloc[
            timezone_dict_to_convert[key].tolist()]['server_name'].tolist()

    averaged_timezone_dict = {}
    for timezone in timezone_dict:
        running_avg = pd.Series(np.zeros(24))
        for server in timezone_dict[timezone]:
            try:
                running_avg += cleaned_server_activity[server]
            except KeyError:
                continue
        # Shift by UTC values
        running_avg = running_avg / len(timezone_dict[timezone])
        index = running_avg.index.values.tolist()
        index = list(map(lambda x: (x + time_shift[timezone]) % 24, index))
        running_avg.index = index
        running_avg = running_avg.sort_index()
        averaged_timezone_dict[timezone] = running_avg

    for timezone in averaged_timezone_dict:
        averaged_timezone_dict[timezone] = averaged_timezone_dict[timezone].replace(0, np.nan).interpolate('index')
    pickle.dump(averaged_timezone_dict, open("timezone_series_{}.p".format(continent_abb), 'wb'))

#
#
# # US
# blizz_realms_us = pickle.load(open('blizz_realms_us.p', 'rb'))['realms']
# blizz_realms_and_timezone_us = [(blizz_realms_us[i]['name'], blizz_realms_us[i]['timezone'])
#                                 for i in range(len(list(blizz_realms_us)))]
# blizz_realms_and_timezone_us = pd.DataFrame(blizz_realms_and_timezone_us, columns=['server_name', 'timezone'])
# timezone_dict = blizz_realms_and_timezone_us.groupby("timezone").groups
#
# # Create a dict with timezone as key and server names as values (indestead of index)
# timezone_dict_to_convert = deepcopy(timezone_dict)
# timezone_dict = {}
# for key in timezone_dict_to_convert.keys():
#     timezone_dict[key] = blizz_realms_and_timezone_us.iloc[
#         timezone_dict_to_convert[key].tolist()]['server_name'].tolist()
#
# averaged_timezone_dict = {}
# for timezone in timezone_dict:
#     running_avg = pd.Series(np.zeros(24))
#     for server in timezone_dict[timezone]:
#         try:
#             running_avg += cleaned_server_activity[server]
#         except KeyError:
#             continue
#     # Shift by UTC values
#     running_avg = running_avg / len(timezone_dict[timezone])
#     index = running_avg.index.values.tolist()
#     index = list(map(lambda x: (x + time_shift[timezone]) % 24, index))
#     running_avg.index = index
#     running_avg = running_avg.sort_index()
#     averaged_timezone_dict[timezone] = running_avg
#
# for timezone in averaged_timezone_dict:
#     averaged_timezone_dict[timezone] = averaged_timezone_dict[timezone].replace(0, np.nan).interpolate('index')
# pickle.dump(averaged_timezone_dict, open("timezone_series_us.p", 'wb'))
#
#
# # EU
# cleaned_server_activity = pickle.load(open('cleaned_server_activity.p', 'rb'))
# blizz_realms_eu = pickle.load(open('blizz_realms_eu.p', 'rb'))['realms']
# blizz_realms_and_timezone_eu = [(blizz_realms_eu[i]['name'], blizz_realms_eu[i]['locale'])
#                                 for i in range(len(list(blizz_realms_eu)))]
# blizz_realms_and_timezone_eu = pd.DataFrame(blizz_realms_and_timezone_eu, columns=['server_name', 'locale'])
# timezone_dict = blizz_realms_and_timezone_eu.groupby("locale").groups
# blizz_server_names = blizz_realms_and_timezone_eu['server_name'].tolist()
#
# # Create a dict with locale as key and server names as values (indestead of index)
# timezone_dict_to_convert = deepcopy(timezone_dict)
# timezone_dict = {}
# for key in timezone_dict_to_convert.keys():
#     timezone_dict[key] = blizz_realms_and_timezone_eu.iloc[
#         timezone_dict_to_convert[key].tolist()]['server_name'].tolist()
#
# averaged_timezone_dict = {}
# for timezone in timezone_dict:
#     running_avg = pd.Series(np.zeros(24))
#     for server in timezone_dict[timezone]:
#         try:
#             running_avg += cleaned_server_activity[server]
#         except KeyError:
#             try:
#                 server = didYouMean(server, cleaned_server_activity.keys())
#                 running_avg += cleaned_server_activity[server]
#             except KeyError:
#                 continue
#     running_avg = running_avg / len(timezone_dict[timezone])
#     index = running_avg.index.values.tolist()
#     index = list(map(lambda x: (x + time_shift[timezone]) % 24, index))
#     running_avg.index = index
#     running_avg = running_avg.sort_index()
#     averaged_timezone_dict[timezone] = running_avg
#
# for timezone in averaged_timezone_dict:
#     averaged_timezone_dict[timezone] = averaged_timezone_dict[timezone].replace(0, np.nan).interpolate('index')
# pickle.dump(averaged_timezone_dict, open('timezone_series_eu.p', 'wb'))

# Merge and convert index to datetime


format_for_visualization(cleaned_server_activity, 'timezone', 'us')
format_for_visualization(cleaned_server_activity, 'locale', 'eu')

series_us = pickle.load(open('timezone_series_us.p', 'rb'))
series_eu = pickle.load(open('timezone_series_eu.p', 'rb'))
master_df = pd.DataFrame(dict(series_us, **series_eu))
master_df.index = list(map(lambda x: datetime(2018, 12, 10, x,), range(24)))

# Add some extra values to make animation smoother
expanding_df = pd.DataFrame(index=pd.date_range(start='2018-12-10', end='2018-12-11', freq='Min'))
master_df = pd.merge(expanding_df, master_df, left_index=True, right_index=True, how='outer').interpolate()
pickle.dump(master_df, open('master_df.p', 'wb'))
