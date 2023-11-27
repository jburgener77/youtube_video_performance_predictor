# Data Exploration from Cleaned Data

## Setup

Previously we cleaned the video_metrics_df and video_comments_df tables and uploaded them to Google's BigQuery platform. This platform allows us to utilize the cloud to perform SQL operations.

First we need to install and import Google's BigQuery library which allows us to call the API and access the uploaded data.

Next, a Google service account needs to be created to access the BigQuery database we created. To do that I followed the insturctions [here](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries).

We can confirm that the BigQuery API is working by previewing writing a SQL command to preview all the rows of the video_metrics_cleaned table.


```python
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import config as cfg
import os

sa_credentials = 'gpc/youtube-scraper-404402-a6dc21ea107a.json' # download from service_account page
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_credentials

credentials = service_account.Credentials.from_service_account_file(
    sa_credentials, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

query_string = """

SELECT * FROM youtube-scraper-404402.yt_data.video_metrics_cleaned LIMIT 5

"""

bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
df = bq_client.query(query_string).to_dataframe()

df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>int64_field_0</th>
      <th>channel_name</th>
      <th>video_id</th>
      <th>title</th>
      <th>published_at</th>
      <th>description</th>
      <th>thumbnail_url</th>
      <th>tags</th>
      <th>category_id</th>
      <th>duration</th>
      <th>view_count</th>
      <th>like_count</th>
      <th>fav_count</th>
      <th>comment_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3</td>
      <td>Why I Salty</td>
      <td>K3s5zrG4t1c</td>
      <td>Got a Job for you, 621: Mission 11 | Armored C...</td>
      <td>2023-11-12 05:00:08+00:00</td>
      <td>#armoredcore6 #bobthebuilder \n\nAI can only d...</td>
      <td>https://i.ytimg.com/vi/K3s5zrG4t1c/default.jpg</td>
      <td>['armored core', 'Gundam', 'Anime', 'ac6', 'Ga...</td>
      <td>20</td>
      <td>PT1M23S</td>
      <td>4829</td>
      <td>549</td>
      <td>0</td>
      <td>50</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>Why I Salty</td>
      <td>HypJk4azqAE</td>
      <td>Pepperidge Farm Remember | Armored Core VI</td>
      <td>2023-11-11 03:58:05+00:00</td>
      <td>#armoredcore6 #familyguy #asmongold \n\nJust t...</td>
      <td>https://i.ytimg.com/vi/HypJk4azqAE/default.jpg</td>
      <td>['armored core', 'Gundam', 'Anime', 'ac6', 'Ga...</td>
      <td>20</td>
      <td>PT22S</td>
      <td>2524</td>
      <td>239</td>
      <td>0</td>
      <td>24</td>
    </tr>
    <tr>
      <th>2</th>
      <td>14</td>
      <td>Why I Salty</td>
      <td>tsmFLhITvGY</td>
      <td>Got a Job for you, 621: Mission 10 | Armored C...</td>
      <td>2023-11-04 04:00:25+00:00</td>
      <td>#armoredcore6 @SpongeBobOfficial \n\nDecided t...</td>
      <td>https://i.ytimg.com/vi/tsmFLhITvGY/default.jpg</td>
      <td>['armored core', 'Gundam', 'Anime', 'ac6', 'Ga...</td>
      <td>20</td>
      <td>PT2M3S</td>
      <td>7127</td>
      <td>613</td>
      <td>0</td>
      <td>37</td>
    </tr>
    <tr>
      <th>3</th>
      <td>17</td>
      <td>Why I Salty</td>
      <td>qls8YCcN8T4</td>
      <td>WE DID IT!  Asmongold Reacted to EP3</td>
      <td>2023-11-01 21:05:17+00:00</td>
      <td>#armoredcore6 #asmongold #mcdonalds \n\nI neve...</td>
      <td>https://i.ytimg.com/vi/qls8YCcN8T4/default.jpg</td>
      <td>['armored core', 'Gundam', 'Anime', 'ac6', 'Ga...</td>
      <td>20</td>
      <td>PT8M37S</td>
      <td>6187</td>
      <td>912</td>
      <td>0</td>
      <td>61</td>
    </tr>
    <tr>
      <th>4</th>
      <td>19</td>
      <td>Why I Salty</td>
      <td>Hv_dkdAp8SQ</td>
      <td>Not Part of Your World | Armored Core VI</td>
      <td>2023-11-01 05:36:37+00:00</td>
      <td>#armoredcore6 \n\nWhen i made the meme "Booty ...</td>
      <td>https://i.ytimg.com/vi/Hv_dkdAp8SQ/default.jpg</td>
      <td>['armored core', 'Gundam', 'Anime', 'ac6', 'Ga...</td>
      <td>20</td>
      <td>PT1M29S</td>
      <td>9400</td>
      <td>939</td>
      <td>0</td>
      <td>91</td>
    </tr>
  </tbody>
</table>
</div>



## Data Exploration by SQL

Now let's look at a couple queries:
1. What is the average view count based on category?
2. How many views, likes, and comments did videos gain per year?
3. What are the top 10 videos by views?
4. How many viewers have commented on multiple videos?


```python
query_string = """
SELECT 
    REPLACE(), 
    COUNT(*) AS total_videos,
    AVG(view_count) AS average_views,
    AVG(like_count) AS average_likes,
    AVG(comment_count) AS average_total_comments
FROM youtube-scraper-404402.yt_data.video_metrics_cleaned
GROUP BY category_id
"""
bq_client.query(query_string).to_dataframe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>category_id</th>
      <th>total_videos</th>
      <th>average_views</th>
      <th>average_likes</th>
      <th>average_total_comments</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20</td>
      <td>502</td>
      <td>2345.304781</td>
      <td>147.88247</td>
      <td>11.669323</td>
    </tr>
    <tr>
      <th>1</th>
      <td>24</td>
      <td>6</td>
      <td>167.000000</td>
      <td>12.50000</td>
      <td>1.333333</td>
    </tr>
  </tbody>
</table>
</div>




```python
query_string = """
SELECT 
    EXTRACT(YEAR FROM published_at) AS publish_year,
    COUNT(*) AS total_videos,
    SUM(view_count) AS total_views,
    SUM(like_count) AS total_likes,
    SUM(fav_count) AS total_favs,
    SUM(comment_count) as total_comments
FROM youtube-scraper-404402.yt_data.video_metrics_cleaned
GROUP BY publish_year
ORDER BY publish_year
"""
bq_client.query(query_string).to_dataframe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>publish_year</th>
      <th>total_videos</th>
      <th>total_views</th>
      <th>total_likes</th>
      <th>total_favs</th>
      <th>total_comments</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019</td>
      <td>30</td>
      <td>8683</td>
      <td>247</td>
      <td>0</td>
      <td>35</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020</td>
      <td>138</td>
      <td>55676</td>
      <td>1712</td>
      <td>0</td>
      <td>406</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2021</td>
      <td>103</td>
      <td>45974</td>
      <td>1615</td>
      <td>0</td>
      <td>254</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2022</td>
      <td>78</td>
      <td>39075</td>
      <td>1550</td>
      <td>0</td>
      <td>241</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2023</td>
      <td>159</td>
      <td>1028937</td>
      <td>69188</td>
      <td>0</td>
      <td>4930</td>
    </tr>
  </tbody>
</table>
</div>




```python
query_string = """
SELECT 
    title,
    view_count
FROM youtube-scraper-404402.yt_data.video_metrics_cleaned
ORDER BY view_count DESC
LIMIT 10
"""
bq_client.query(query_string).to_dataframe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>view_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Raven Don't Listen to Ayre (A.I Voice Test).</td>
      <td>169898</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Raven Please... | Armored Core VI</td>
      <td>107156</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Your Next Target, 621 | Asmongold Reacts</td>
      <td>66195</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Got a Job for you, 621: Mission 1 | Armored Co...</td>
      <td>61226</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Got a Job for you, 621: Mission 2 | Armored Co...</td>
      <td>59181</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Got a Job for you, 621: Mission 0 | Armored Co...</td>
      <td>56188</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Booty Call | Armored Core VI</td>
      <td>36502</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Express Delivery | Armored Core VI</td>
      <td>34016</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Was it worth it Raven? | Armored Core VI</td>
      <td>31429</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Hey Buddy | Armored Core VI</td>
      <td>28623</td>
    </tr>
  </tbody>
</table>
</div>




```python
query_string = """
SELECT 
    video_comment_user,
    COUNT(video_comment_user) AS total_comments,
    COUNT(DISTINCT video_id) AS number_of_videos
FROM youtube-scraper-404402.yt_data.video_comments_cleaned
WHERE video_comment_user <> 'Why I Salty'
GROUP BY video_comment_user
ORDER BY total_comments DESC
LIMIT 10
"""
bq_client.query(query_string).to_dataframe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>video_comment_user</th>
      <th>total_comments</th>
      <th>number_of_videos</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>jPaolo</td>
      <td>70</td>
      <td>63</td>
    </tr>
    <tr>
      <th>1</th>
      <td>taylormadetactics</td>
      <td>48</td>
      <td>42</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Dizzy[sic]</td>
      <td>46</td>
      <td>40</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Mirage Nikita</td>
      <td>25</td>
      <td>18</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Yossa</td>
      <td>25</td>
      <td>21</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Eternal &amp;Misery</td>
      <td>25</td>
      <td>22</td>
    </tr>
    <tr>
      <th>6</th>
      <td>HonzaLuH</td>
      <td>21</td>
      <td>17</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Harold Thomas</td>
      <td>14</td>
      <td>9</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ÇakmakÇakmak</td>
      <td>14</td>
      <td>11</td>
    </tr>
    <tr>
      <th>9</th>
      <td>naniii?</td>
      <td>14</td>
      <td>14</td>
    </tr>
  </tbody>
</table>
</div>



## Data Exploration by Pandas/Matplotlib

Now let's read in both files as Pandas dataframes and plot some comparisons between metrics.


```python
query_string = """
SELECT 
    *
FROM youtube-scraper-404402.yt_data.video_metrics_cleaned
"""
video_metrics_df = bq_client.query(query_string).to_dataframe()

query_string = """
SELECT 
    *
FROM youtube-scraper-404402.yt_data.video_comments_cleaned
"""
video_comments_df = bq_client.query(query_string).to_dataframe()
```

How do the video metrics correlate with each other? How are they distributed?


```python
from matplotlib import pyplot as plt
import seaborn as sns
```


```python

plot_df = video_metrics_df[['view_count', 'comment_count', 'like_count']].copy()
plot_df = plot_df.astype('float64')
g = sns.PairGrid(plot_df)
g.map_diag(sns.kdeplot)
g.map_lower(sns.scatterplot)
g.map_upper(sns.kdeplot)

g.axes[0,0].set_ylabel('No. Views')
g.axes[1,0].set_ylabel('No. Comments')
g.axes[2,0].set_ylabel('No. Likes')

g.axes[2,0].set_xlabel('No. Views')
g.axes[2,1].set_xlabel('No. Comments')
g.axes[2,2].set_xlabel('No. Likes')

g.fig.suptitle('Channel Video Metrics', y=1)
```




    Text(0.5, 1, 'Channel Video Metrics')




    
![png](output_18_1.png)
    


There seem to be some extreme outliers, does standardizing the data help?


```python
from scipy import stats
import numpy as np

for col in plot_df:
    z_score = stats.zscore(plot_df[col].values)
    plot_df[f'{col}_zscore'] = z_score
    print(f'z score generated for {col}')
```

    z score generated for view_count
    z score generated for comment_count
    z score generated for like_count
    z score generated for view_count_zscore
    z score generated for comment_count_zscore
    z score generated for like_count_zscore
    


```python
vars = ['view_count_zscore', 'comment_count_zscore', 'like_count_zscore']
g = sns.PairGrid(plot_df, vars=vars)
g.map_diag(sns.kdeplot)
g.map_lower(sns.scatterplot)
g.map_upper(sns.kdeplot)

g.axes[0,0].set_ylabel('No. Views (Scaled)')
g.axes[1,0].set_ylabel('No. Comments (Scaled)')
g.axes[2,0].set_ylabel('No. Likes (Scaled)')

g.axes[2,0].set_xlabel('No. Views (Scaled)')
g.axes[2,1].set_xlabel('No. Comments (Scaled)')
g.axes[2,2].set_xlabel('No. Likes (Scaled)')
g.fig.suptitle('Channel Video Metrics (Scaled)', y=1)
```




    Text(0.5, 1, 'Channel Video Metrics (Scaled)')




    
![png](output_21_1.png)
    


As expected, video metrics are stronlgy correlated with one another and likely reflects viewer engagement.

Can we get a sense of how views are distributed between videos with engagement (viewer comments) vs. non-engagement? (no viewer comments).


```python
engaged_viewship = [
    plot_df[plot_df['comment_count'] > 0]['view_count'].values,
    plot_df[plot_df['comment_count'] == 0]['view_count'].values
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

bplot1 = ax1.boxplot(engaged_viewship, patch_artist=True, notch=True)
ax1.set_xticklabels(['Engagement', 'No Engagement'])

bplot2= ax2.boxplot(engaged_viewship, patch_artist=True, notch=True)
ax2.set_xticklabels(['Engagement', 'No Engagement'])

colors = ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]

for bplot in (bplot1, bplot2):
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

plot_min = np.min([x for sublist in engaged_viewship for x in sublist])
plot_max = np.quantile([x for sublist in engaged_viewship for x in sublist], 0.9)

ax2.set_ylim(plot_min-10,plot_max)
ax1.set_ylabel('No. Views')

ax1.set_title('All Views')
ax2.set_title('Views below 90th Percentile')

fig.suptitle('Views based on Viewer Engagement')

plt.show()
```


    
![png](output_23_0.png)
    


Interestingly there doesn't seem to be a clear separation in views between videos with or without user engagement. Perhaps there are other factors that contribute to this that requires further refinement of the data.
