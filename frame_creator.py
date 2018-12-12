import pickle
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from datetime import datetime
from tqdm import tqdm
from sklearn import preprocessing


master_df = pickle.load(open('master_df.p', 'rb'))
master_df = master_df.iloc[::3]  # Only use every third minute


def plot(df, ax, date):
    colors = {'America/Chicago': '#02b3e4',
              'America/Denver': '#f95c3c',
              'America/Los_Angeles': '#b86565',
              'America/New_York': '#adc9bf',
              'America/Sao_Paulo': '#ffc7fd',
              'Australia/Melbourne': '#ea3737',
              'de_DE': "#0091ac",
              'en_GB': "#009980",
              'es_ES': "#ff813c",
              'fr_FR': "#ffffe5",
              'it_IT': "#807dba",
              'pt_PT': "#737373",
              'ru_RU': "#230827"}
    coordinates_lat_long = {'America/Chicago': (41.881832, -87.623177),
                            'America/Denver': (39.7392358, -104.990251),
                            'America/Los_Angeles': (34.052235, -118.243683),
                            'America/New_York': (40.730610, -73.935242),
                            'America/Sao_Paulo': (-23.533773, -46.625290),
                            'Australia/Melbourne': (-37.815018, 144.946014),
                            'de_DE': (52.520008, 13.404954),
                            'en_GB': (51.509865, -0.118092),
                            'es_ES': (40.416775, -3.703790),
                            'fr_FR': (48.864716, 2.349014),
                            'it_IT': (41.890251, 12.492373),
                            'pt_PT': (38.736946, -9.142685),
                            'ru_RU': (55.751244, 37.618423)}
    fontname = 'Avenir'
    fontsize = 28
    date_x = -10
    date_y = -50
    if ax is None:
        fig = plt.figure(figsize=(19.2, 10.8))
        ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,
                                               min_latitude=-65,
                                               max_latitude=70))
    os.environ["CARTOPY_USER_BACKGROUNDS"] = "/anaconda3/envs/wow/lib/python3.7/site-packages/cartopy/BG/"
    ax.background_img(name='BM', resolution='low')
    ax.set_extent([-170, 179, -65, 70], crs=ccrs.PlateCarree())
    ax.text(date_x, date_y,
            f"{date.strftime('%H:%M UTC')}",
            color='white',
            fontname=fontname, fontsize=fontsize * 1.3,
            transform=ccrs.PlateCarree())

    for timezone in df:
        lats = coordinates_lat_long[timezone][0]
        longs = coordinates_lat_long[timezone][1]

        x = df[timezone].loc[date]
        #         min_max_scaler = preprocessing.MinMaxScaler()
        #         x_scaled = min_max_scaler.fit_transform(np.reshape(x,(-1,1)))
        sizes = np.log(x + 0.0001) * 1500

        ax.scatter(longs, lats, s=sizes.astype(int),
                   color=colors[timezone], alpha=0.8,
                   transform=ccrs.PlateCarree())


fig = plt.figure(figsize=(19.2, 10.8))
ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,
                                       min_latitude=-65,
                                       max_latitude=70))
for i, timestamp in enumerate(tqdm(list(master_df.index))):
    plot(master_df, ax, timestamp)
    fig.tight_layout(pad=-0.5)
    fig.savefig(f"frames/frame_{i}.png", dpi=100,
                frameon=False, facecolor='black')
    ax.clear()
