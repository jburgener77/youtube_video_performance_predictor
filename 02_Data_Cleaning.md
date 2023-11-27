# Data Cleaning from Gathered Data

## Setup

Here we'll use some of the same libraries to clean the data gathered from the YouTube API.


```python
import pandas as pd
import numpy as np
```


```python
video_metrics_df = pd.read_csv('csv/video_metrics.csv', index_col=0)
video_comments_df = pd.read_csv('csv/video_comments.csv', index_col=0)
print(f'video_metrics_df shape: {video_metrics_df.shape}')
print(f'video_comments_df shape: {video_comments_df.shape}')
```

    video_metrics_df shape: (508, 13)
    video_comments_df shape: (2192, 6)
    

## Cleaning

First let's look at the video_metrics_df


```python
video_metrics_df.dtypes
```




    channel_name     object
    video_id         object
    title            object
    published_at     object
    description      object
    thumbnail_url    object
    tags             object
    category_id       int64
    duration         object
    view_count        int64
    like_count        int64
    fav_count         int64
    comment_count     int64
    dtype: object



Based on the above, it looks like that most columns are the expected type; numerical values are integers, strings are objects. 'published_at' and 'duration' should ideally be datetime format, but since we plan to upload these cleaned CSV files to a SQL database we'll refrain for now. 'category_id' should be an object rather than an integer since these values correspond with a separate table that links each category_id to a category name.


```python
video_metrics_df['category_id'] = video_metrics_df['category_id'].astype('str')
print(video_metrics_df['category_id'].describe())
```

    count     508
    unique      2
    top        20
    freq      502
    Name: category_id, dtype: object
    

Now if we look at the categorical features further.


```python
video_metrics_df.describe(include=['O'])
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
      <th>channel_name</th>
      <th>video_id</th>
      <th>title</th>
      <th>published_at</th>
      <th>description</th>
      <th>thumbnail_url</th>
      <th>tags</th>
      <th>category_id</th>
      <th>duration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>508</td>
      <td>508</td>
      <td>508</td>
      <td>508</td>
      <td>490</td>
      <td>508</td>
      <td>508</td>
      <td>508</td>
      <td>508</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>1</td>
      <td>508</td>
      <td>505</td>
      <td>508</td>
      <td>461</td>
      <td>508</td>
      <td>46</td>
      <td>2</td>
      <td>466</td>
    </tr>
    <tr>
      <th>top</th>
      <td>Why I Salty</td>
      <td>Sd34QHPBKRA</td>
      <td>Salty Brew - Creation Control [Eternal Card Game]</td>
      <td>2023-09-30T20:44:24Z</td>
      <td>Powered by Restream https://restream.io\n\nJus...</td>
      <td>https://i.ytimg.com/vi/ezJOf4Zn0Os/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT1M</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>508</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>9</td>
      <td>1</td>
      <td>289</td>
      <td>502</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



We can see that most columns have unique entries, as each row represents a unique video. We also expect the tags, description, and category IDs to be re-used at times. Interestingly the title of the video appears to be duplicated for a few videos - let's explore why that may be the case.


```python
duplicated_titles = video_metrics_df[video_metrics_df['title'].duplicated()]['title']
print(duplicated_titles.to_list())
video_metrics_df[video_metrics_df['title'].isin(duplicated_titles)]
```

    ['Mecha Auto Battler and then some Armored Core | Mechabellum [STREAM]', 'Salty Brew - BULL$%@T XENAN STRANGERS [Eternal Card Game]', 'Salty Brew - Creation Control [Eternal Card Game]']
    




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
      <th>47</th>
      <td>Why I Salty</td>
      <td>-UrQ--njWvY</td>
      <td>Mecha Auto Battler and then some Armored Core ...</td>
      <td>2023-10-15T19:39:11Z</td>
      <td>Was just mainly going to do a Mecabellum strea...</td>
      <td>https://i.ytimg.com/vi/-UrQ--njWvY/default_liv...</td>
      <td>['mecha', 'auto battler', 'tft', 'team fight t...</td>
      <td>20</td>
      <td>P0D</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>48</th>
      <td>Why I Salty</td>
      <td>DfV-xuJX6bE</td>
      <td>Mecha Auto Battler and then some Armored Core ...</td>
      <td>2023-10-14T05:24:00Z</td>
      <td>Was just mainly going to do a Mecabellum strea...</td>
      <td>https://i.ytimg.com/vi/DfV-xuJX6bE/default.jpg</td>
      <td>['mecha', 'auto battler', 'tft', 'team fight t...</td>
      <td>20</td>
      <td>PT2H20M31S</td>
      <td>337</td>
      <td>13</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>443</th>
      <td>Why I Salty</td>
      <td>mRR2JQjzidE</td>
      <td>Salty Brew - BULL$%@T XENAN STRANGERS [Eternal...</td>
      <td>2020-03-09T00:57:49Z</td>
      <td>I got home late from work and decided stream a...</td>
      <td>https://i.ytimg.com/vi/mRR2JQjzidE/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT32M51S</td>
      <td>434</td>
      <td>10</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>445</th>
      <td>Why I Salty</td>
      <td>DuMKMM0vFj0</td>
      <td>Salty Brew - BULL$%@T XENAN STRANGERS [Eternal...</td>
      <td>2020-03-05T06:15:04Z</td>
      <td>Warning there is only one match, but it very l...</td>
      <td>https://i.ytimg.com/vi/DuMKMM0vFj0/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT23M29S</td>
      <td>290</td>
      <td>5</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>446</th>
      <td>Why I Salty</td>
      <td>b3R1TBYyB28</td>
      <td>Salty Brew - Creation Control [Eternal Card Game]</td>
      <td>2020-03-04T05:46:33Z</td>
      <td>Decided to give creation control another go, b...</td>
      <td>https://i.ytimg.com/vi/b3R1TBYyB28/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT33M25S</td>
      <td>466</td>
      <td>20</td>
      <td>0</td>
      <td>5</td>
    </tr>
    <tr>
      <th>459</th>
      <td>Why I Salty</td>
      <td>Snk0gfToLYY</td>
      <td>Salty Brew - Creation Control [Eternal Card Game]</td>
      <td>2020-02-15T05:05:54Z</td>
      <td>Originally i was trying to make an armory deck...</td>
      <td>https://i.ytimg.com/vi/Snk0gfToLYY/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT32M2S</td>
      <td>305</td>
      <td>9</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Nothing unusual here, all duplicated titles have different values in other columns. 

The only exception is the first set of videos which share the same title and description, but since these were from steams on back-to-back days most likely the title was re-used.

Finally let's look for missing values.


```python
print(video_metrics_df.isna().sum())
```

    channel_name      0
    video_id          0
    title             0
    published_at      0
    description      18
    thumbnail_url     0
    tags              0
    category_id       0
    duration          0
    view_count        0
    like_count        0
    fav_count         0
    comment_count     0
    dtype: int64
    


```python
video_metrics_df[video_metrics_df['description'].isna()].head()
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
      <th>63</th>
      <td>Why I Salty</td>
      <td>xUOy06kZMAw</td>
      <td>Raven Please..</td>
      <td>2023-10-01T21:08:07Z</td>
      <td>NaN</td>
      <td>https://i.ytimg.com/vi/xUOy06kZMAw/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT59S</td>
      <td>9259</td>
      <td>638</td>
      <td>0</td>
      <td>21</td>
    </tr>
    <tr>
      <th>67</th>
      <td>Why I Salty</td>
      <td>yRCX_zCiBZ0</td>
      <td>Got a Job For you 621 (5) #armoredcore6 #armor...</td>
      <td>2023-09-30T20:57:58Z</td>
      <td>NaN</td>
      <td>https://i.ytimg.com/vi/yRCX_zCiBZ0/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT1M</td>
      <td>4729</td>
      <td>498</td>
      <td>0</td>
      <td>22</td>
    </tr>
    <tr>
      <th>68</th>
      <td>Why I Salty</td>
      <td>rZdzszUyav8</td>
      <td>Got a Job For you 621 (4) #armoredcore6 #armor...</td>
      <td>2023-09-30T20:44:24Z</td>
      <td>NaN</td>
      <td>https://i.ytimg.com/vi/rZdzszUyav8/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT49S</td>
      <td>4742</td>
      <td>524</td>
      <td>0</td>
      <td>16</td>
    </tr>
    <tr>
      <th>69</th>
      <td>Why I Salty</td>
      <td>1vSUQfUB66Q</td>
      <td>Got a Job For you 621 (3) #armoredcore6 #armor...</td>
      <td>2023-09-30T20:29:00Z</td>
      <td>NaN</td>
      <td>https://i.ytimg.com/vi/1vSUQfUB66Q/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT17S</td>
      <td>3894</td>
      <td>242</td>
      <td>0</td>
      <td>6</td>
    </tr>
    <tr>
      <th>70</th>
      <td>Why I Salty</td>
      <td>9Er61UwlIF4</td>
      <td>Got A Job For You 621 (1) #armoredcore6 #armor...</td>
      <td>2023-09-30T20:09:57Z</td>
      <td>NaN</td>
      <td>https://i.ytimg.com/vi/9Er61UwlIF4/default.jpg</td>
      <td>none</td>
      <td>20</td>
      <td>PT15S</td>
      <td>3177</td>
      <td>242</td>
      <td>0</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



Doing a quick check on YouTube shows that NaN values correspond with videos that had no description provided. We'll update this as 'No description provided' to remove any confusion.


```python
video_metrics_df['description'] = video_metrics_df['description'].replace(np.nan, 'No description provided')
print(video_metrics_df['description'].describe())
```

    count                         508
    unique                        462
    top       No description provided
    freq                           18
    Name: description, dtype: object
    

Now let's repeat the process with the video_comments_df.


```python
video_comments_df.dtypes
```




    video_id                   object
    video_comment              object
    video_comment_user         object
    video_comment_time         object
    video_comment_parent_id    object
    video_comment_child_id     object
    dtype: object




```python
video_comments_df.describe()
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
      <th>video_id</th>
      <th>video_comment</th>
      <th>video_comment_user</th>
      <th>video_comment_time</th>
      <th>video_comment_parent_id</th>
      <th>video_comment_child_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>2192</td>
      <td>2044</td>
      <td>2043</td>
      <td>2044</td>
      <td>2044</td>
      <td>2044</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>508</td>
      <td>2016</td>
      <td>918</td>
      <td>2044</td>
      <td>1536</td>
      <td>509</td>
    </tr>
    <tr>
      <th>top</th>
      <td>t3y4vt9kkoc</td>
      <td>Nice</td>
      <td>Why I Salty</td>
      <td>2020-07-11T15:34:16Z</td>
      <td>UgyB03KENb3uiX5Zafx4AaABAg</td>
      <td>0</td>
    </tr>
    <tr>
      <th>freq</th>
      <td>36</td>
      <td>5</td>
      <td>252</td>
      <td>1</td>
      <td>6</td>
      <td>1536</td>
    </tr>
  </tbody>
</table>
</div>




```python
print(video_metrics_df.isna().sum())
```

    channel_name     0
    video_id         0
    title            0
    published_at     0
    description      0
    thumbnail_url    0
    tags             0
    category_id      0
    duration         0
    view_count       0
    like_count       0
    fav_count        0
    comment_count    0
    dtype: int64
    

Everything looks good! Lets save these tables and ingest into a SQL database for subsequent analysis


```python
video_comments_df.to_csv('csv/video_metrics_cleaned.csv')
video_metrics_df.to_csv('csv/video_metrics_cleaned.csv')
```
