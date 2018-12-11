import re
import pickle


# Loads a dictionary where you get a tuple of server name and server activity as a pandas df by id
wacraft_server_activity = pickle.load(open("crawled_server_activity.p", 'rb'))

servername_and_dataframe = []
for key in wacraft_server_activity:
    server_name = wacraft_server_activity[key][0]
    dataframe = wacraft_server_activity[key][1]
    dataframe = dataframe.drop(["alliance_entries", 'horde_entries'], axis=1).astype(int, copy=False)
    servername_and_dataframe.append((server_name, dataframe))


# Get names from wacraftrealms.com in a cleaner way
from_list_to_dict = servername_and_dataframe
servername_and_dataframe = {}
for server_df_tuple in from_list_to_dict:
    cleaned_name = (re.sub(r" - [A-Z]{2,}", '', server_df_tuple[0]))
    servername_and_dataframe[cleaned_name] = server_df_tuple[1]
cleaned_server_names = [re.sub(r" - [A-Z]{2,}", '', server_name) for server_name,_ in from_list_to_dict]

# Remove completely empty dataframes
empty_dfs = [key for key in servername_and_dataframe if
             servername_and_dataframe[key].isin([0]).all().all()]
for key in empty_dfs:
    servername_and_dataframe.pop(key)

pickle.dump(servername_and_dataframe, open('cleaned_server_activity.p', 'wb'))
