# Data Mining from Youtube Channels

## Setup
Import required packages including Google's API for Youtube. For more information please see: https://developers.google.com/youtube/v3


```python
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from yt_api_jb import YtScraper
```

Here we'll look at my brother's Youtube channel, WhyISalty.

A Google Account is required to access the Google API Console. For this project, an application was created using the [Google Developers Console](https://console.developers.google.com/).

Now let's import the YtScraper class and create an object that contains information and methods related to the WhyISalty channel:


```python
# Call the Youtube API Scraper and list all videos WhyISalty's Youtube channel
yt_whyisalty = YtScraper()
video_ids = yt_whyisalty.get_upload_ids("WhyISalty")
print(video_ids[0:6]) # First 5 video ids
```

    ['HqNMNXa7REY', 'P1a3DEpvFeE', 'FK0gxnwyhew', 'K3s5zrG4t1c', 'HypJk4azqAE', 'JFs_hiTaU9M']
    

Each ID above corresponds to a Video or Live Stream uploaded by the User. We can also get the total statistics across all videos:


```python
channel_metrics_df = yt_whyisalty.metrics
print(channel_metrics_df)
```

      viewCount subscriberCount  hiddenSubscriberCount videoCount  \
    0   1173778            7460                  False        507   
    
                                           thumbnail_url channel_name  
    0  https://yt3.ggpht.com/7jNjyWBlUgVNiFBfzigXaH9K...  Why I Salty  
    

## Data Mining


```python
video_metric_df = yt_whyisalty.get_video_metrics(video_ids)
print(video_metric_df.head())
```

      channel_name     video_id  \
    0  Why I Salty  HqNMNXa7REY   
    1  Why I Salty  P1a3DEpvFeE   
    2  Why I Salty  FK0gxnwyhew   
    3  Why I Salty  K3s5zrG4t1c   
    4  Why I Salty  HypJk4azqAE   
    
                                                   title          published_at  \
    0  Quest to Hunt Brachydios | Monster Hunter Worl...  2023-11-15T03:27:18Z   
    1  Grinding for Bow Gear | Monster Hunter World [...  2023-11-14T01:57:06Z   
    2   It's Hammer TIme | Monster Hunter World [STREAM]  2023-11-13T01:10:44Z   
    3  Got a Job for you, 621: Mission 11 | Armored C...  2023-11-12T05:00:08Z   
    4         Pepperidge Farm Remember | Armored Core VI  2023-11-11T03:58:05Z   
    
                                             description  \
    0  Powered by Restream https://restream.io\n\nJus...   
    1  Powered by Restream https://restream.io\n\nJus...   
    2  Powered by Restream https://restream.io\n\nJus...   
    3  #armoredcore6 #bobthebuilder \n\nAI can only d...   
    4  #armoredcore6 #familyguy #asmongold \n\nJust t...   
    
                                        thumbnail_url  \
    0  https://i.ytimg.com/vi/HqNMNXa7REY/default.jpg   
    1  https://i.ytimg.com/vi/P1a3DEpvFeE/default.jpg   
    2  https://i.ytimg.com/vi/FK0gxnwyhew/default.jpg   
    3  https://i.ytimg.com/vi/K3s5zrG4t1c/default.jpg   
    4  https://i.ytimg.com/vi/HypJk4azqAE/default.jpg   
    
                                                    tags category_id    duration  \
    0                                               none          20  PT3H58M50S   
    1                                               none          24  PT2H24M49S   
    2                                               none          20   PT5H5M30S   
    3  [armored core, Gundam, Anime, ac6, Gaming, Mec...          20     PT1M23S   
    4  [armored core, Gundam, Anime, ac6, Gaming, Mec...          20       PT22S   
    
      view_count like_count fav_count comment_count  
    0         39          4         0             1  
    1        128         10         0             7  
    2        215         10         0             4  
    3       4829        549         0            50  
    4       2524        239         0            24  
    


```python
video_comments_df = yt_whyisalty.get_video_comments(video_ids)
print(video_comments_df.head())
```

          video_id                                      video_comment  \
    0  HqNMNXa7REY  Good luck trying out the Charge Blade. Transfo...   
    1  P1a3DEpvFeE  Nice, good luck on the rest of your journey, s...   
    2  P1a3DEpvFeE                                       Stream died?   
    3  P1a3DEpvFeE                   lel so it wasn't just me then XD   
    4  P1a3DEpvFeE        @Kuruwa Yoshiko Thought it was my internet.   
    
      video_comment_user    video_comment_time     video_comment_parent_id  \
    0       Gobo KoboObo  2023-11-15T05:10:21Z  UgzWhoTNYW-C1nD1Lm94AaABAg   
    1        Diego Cantu  2023-11-14T03:48:22Z  Ugx5R_BBSeGsBuC3AN54AaABAg   
    2       Gobo KoboObo  2023-11-14T01:46:07Z  Ugx4-6nI0vtlaGv735d4AaABAg   
    3     Kuruwa Yoshiko  2023-11-14T01:47:07Z  Ugx4-6nI0vtlaGv735d4AaABAg   
    4       Gobo KoboObo  2023-11-14T01:50:20Z  Ugx4-6nI0vtlaGv735d4AaABAg   
    
                                  video_comment_child_id  
    0                                                  0  
    1                                                  0  
    2                                                  0  
    3  Ugx4-6nI0vtlaGv735d4AaABAg.9x4SL68zJEO9x4SSUbjmUM  
    4  Ugx4-6nI0vtlaGv735d4AaABAg.9x4SL68zJEO9x4Sp7-cGGN  
    

## Database Creation

Now we'll export both of these tables as separate CSV files. We'll also create a single row CSV file containing the channel metrics to better represent relational databases.


```python
video_metric_df.to_csv('csv/video_metrics.csv')
video_comments_df.to_csv('csv/video_comments.csv')
```
