# World of Wacraft activity map
An animated world map that shows WoW player activity within one

# Functionality
- **Note**: Each steps produces a pickle file that is then picked up by the proceeding step. This is rather unusual but I wanted to make it easy to understand what each step does.
- I used `blizz_api_calls.py` to retrieve the US and EU realm names
- `wacraft_realms_scraper.py` is a scraper that crawls www.wacraftrealms.com to retrieve the server activity of several WoW servers 
- The data from warcraftrealms is then preprocessed by `clean_server_activity.py`
- Then, I use `format_for_visualization` to merge the server activity from www.wacraftrealms.com and the locality information form the Blizzard API to have both information in a single DataFrame saved as
- Finally, `frame_create.py` creates several frames where each frame is one observation of the worldwide WoW server activity. It contains colored blobs where the location of the blob indicates the server location and the size of the blob shows the activity. Larger blobs mean higher activation. You can run the code on `Visulization.ipynb` to see how I patched everything together.
- `wow_activity_video.mov` contains the final video that consists of all beforehand created frames

# Sources
I used http://www.warcraftrealms.com to get access to CensusPlus UI for the WoW activity data and NASA's Blue Marble picture
