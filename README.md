# World of Wacraft activity map
An animated world map that shows WoW player activity within one

# Functionality
- I used `blizz_api_calls.py` to retrieve the US and EU realm names and save them as a pickle file
- `wacraft_realms_scraper.py` is a scraper that crawls www.wacraftrealms.com to retrieve the server activity of several WoW servers and save
- Then, I use `format_for_visualization` to merge the server activity from wacraftrealms.com and the locality information form the Blizzard API to have both information in a single DataFrame
- Finally, `frame_create.py` creates several frames where each frame is one observation of the worldwide WoW server activity. It contains colored blobs where the location of the blob indicates the server location and the size of the blob shows the activity. Larger blobs mean higher activation.
You can run the code on `Visulization.ipynb` to see how I patched everything together.
- `wow_activity_video.mov` contains the final video that consists of all beforehand created frames

# Sources
I used http://www.warcraftrealms.com to get access to CensusPlus UI for the WoW activity data and NASA's Blue Marble picture
