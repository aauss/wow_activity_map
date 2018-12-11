import pickle
import pandas as pd
import numpy as np
from copy import deepcopy

cleaned_series = pickle.load(open('cleaned_server_activity.p', 'rb'))
blizz_realms_us = pickle.load(open('blizz_realms_us.p', 'rb'))['realms']

blizz_realms_and_timezone_us = [(blizz_realms_us[i]['name'], blizz_realms_us[i]['timezone'])
                                for i in range(len(list(blizz_realms_us)))]
blizz_realms_and_timezone_us = pd.DataFrame(blizz_realms_and_timezone_us, columns=['server_name', 'timezone'])
timezone_dict = blizz_realms_and_timezone_us.groupby("timezone").groups

# Create a dict with timezone as key and server names as values (indestead of index)
timezone_dict_to_convert = deepcopy(timezone_dict)
timezone_dict = {}
for key in timezone_dict_to_convert.keys():
    timezone_dict[key] = blizz_realms_and_timezone_us.iloc[
        timezone_dict_to_convert[key].tolist()]['server_name'].tolist()

averaged_timezone_dict = {}
for timezone in timezone_dict:
    running_avg = pd.Series(np.zeros(24))
    for server in timezone_dict[timezone]:
        try:
            running_avg += cleaned_series[server]
        except KeyError:
            continue
    averaged_timezone_dict[timezone] = running_avg / len(timezone_dict[timezone])

for timezone in averaged_timezone_dict:
    averaged_timezone_dict[timezone] = averaged_timezone_dict[timezone].replace(0, np.nan).interpolate('index')
pickle.dump(averaged_timezone_dict, open("timezone_series_us.p", 'wb'))