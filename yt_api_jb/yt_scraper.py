import pandas as pd
from googleapiclient.discovery import build
#import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class YtScraper:
    
    def __init__(self):
        self.build_youtube_api()
    
    def build_youtube_api(self):
        """
        Function that requires a client_secrets_file and scopes. 

        The client_secrets_file can be generated following the documentation located here:
            https://developers.google.com/youtube/v3/getting-started

        Returns:
            youtube: The YouTube v3 API object
        """
        # hard-coded objects within function
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyDkJMCpvXWDq6iVSuGh6Xf_rH_hvcukKMI"
        #scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        # build the API with the provided scopes and credentials
        youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
        '''
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes) # this will cause a new window to pop up and authorize the app
        credentials = flow.run_local_server()
        youtube = build(api_service_name, api_version, credentials=credentials)
        '''

        self.api = youtube
    
    def get_upload_ids(self, channel):
        """
        Returns channel metrics and a list of videoIds uploaded by the provided channel_id
        which can be used in the subsequent functions:
            - get_video_metrics()
            - get_comments_data()

        Args:
            channel_id: channelId - can be generated from get_channel_id
            api_object: created by build_youtube_api()

        Returns:
            channel_metrics: a pandas dataframe with channel_name, total_view_count,
                subscriber_count, video_count, and thumbnail_url
            video_ids: a list of unique videoIds
        """
        def get_channel_id(channel_name, api_object):
            # submit a search request and list channel_id by querying channel_name
            request = api_object.search().list(
                part="snippet",
                maxResults=10,
                q=channel_name
            )
            channel_search = request.execute()
            channel_id = channel_search['items'][0]['id']['channelId']

            return(channel_id)
        
        # get channel statistics and video uploads
        channel_id = get_channel_id(channel, self.api)
        
        request = self.api.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        channel_stats = request.execute()
        playlist_id = channel_stats['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        channel_metrics = channel_stats['items'][0]['statistics']
        channel_metrics_df = pd.DataFrame(channel_metrics, index = [0])
        channel_metrics_df['thumbnail_url'] = channel_stats['items'][0]['snippet']['thumbnails']['default']['url']
        channel_metrics_df['channel_name'] = channel_stats['items'][0]['snippet']['title']

        # view videos under playlistId
        request = self.api.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )
        playlist_items = request.execute()
        video_ids = []
        # get first set of video ideas then move to next page
        for items in playlist_items['items']:
            _video_id = items['snippet']['resourceId']['videoId']
            video_ids.append(_video_id)

        while 'nextPageToken' in playlist_items.keys():
            next_page_token = playlist_items['nextPageToken']
            request = self.api.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            playlist_items = request.execute()
            for items in playlist_items['items']:
                _video_id = items['snippet']['resourceId']['videoId']
                video_ids.append(_video_id)

        self.metrics = channel_metrics_df
        return(video_ids)

    def get_video_metrics(self, video_ids):
        try:
            self.api
        except:
            'No API provided, please ensure you are properly authenticated'
        # initialize video metrics
        channel_name = []
        _video_id = []
        video_title = []
        video_published_at = []
        video_description = []
        video_thumbnail_url = []
        video_tags = []
        video_category_id = []
        video_duration = []
        video_view_count = []
        video_like_count = []
        video_fav_count = []
        video_comment_count = []

        # parse through video_ids list
        for video_id in video_ids:
            request = self.api.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            video_stats = request.execute()
            channel_name.append(video_stats['items'][0]['snippet']['channelTitle'])
            _video_id.append(video_id)
            video_title.append(video_stats['items'][0]['snippet']['title'])
            video_published_at.append(video_stats['items'][0]['snippet']['publishedAt'])
            video_description.append(video_stats['items'][0]['snippet']['description'])
            video_thumbnail_url.append(video_stats['items'][0]['snippet']['thumbnails']['default']['url'])
            if "tags" in video_stats['items'][0]['snippet'].keys():
                video_tags.append(video_stats['items'][0]['snippet']['tags'])
            else:
                video_tags.append('none')
            video_category_id.append(video_stats['items'][0]['snippet']['categoryId'])
            video_duration.append(video_stats['items'][0]['contentDetails']['duration'])
            video_view_count.append(video_stats['items'][0]['statistics']['viewCount'])
            video_like_count.append(video_stats['items'][0]['statistics']['likeCount'])
            video_fav_count.append(video_stats['items'][0]['statistics']['favoriteCount'])
            video_comment_count.append(video_stats['items'][0]['statistics']['commentCount'])

        # append to dataframe
        video_dataframe = pd.DataFrame({
            'channel_name':channel_name,
            'video_id':_video_id,
            'title':video_title,
            'published_at':video_published_at,
            'description':video_description,
            'thumbnail_url':video_thumbnail_url,
            'tags':video_tags,
            'category_id':video_category_id,
            'duration':video_duration,
            'view_count':video_view_count,
            'like_count':video_like_count,
            'fav_count':video_fav_count,
            'comment_count':video_comment_count
        })

        return(video_dataframe)

    def get_video_comments(self, video_ids):
        try:
            self.api
        except:
            'No API provided, please ensure you are properly authenticated'
        # get comments and replies from each video id
        video_id_list = []
        video_comment_text = []
        video_comment_user = []
        video_comment_time = []
        video_comment_parent_id = []
        video_comment_child_id = []

        for video_id in video_ids:
            # check if video has comments
            if (self.get_video_metrics([video_id])['comment_count'] == '0').bool():
                video_id_list.append(video_id)
                video_comment_text.append("NA")
                video_comment_user.append("NA")
                video_comment_time.append("NA")
                video_comment_parent_id.append("NA")
                video_comment_child_id.append("NA")
                continue

            request = self.api.commentThreads().list(
                part="snippet,replies",
                videoId=video_id
            )

            video_comments = request.execute()
            for comment in video_comments['items']:
                video_id_list.append(comment['snippet']['videoId'])
                video_comment_text.append(comment['snippet']['topLevelComment']['snippet']['textOriginal'])
                video_comment_user.append(comment['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                video_comment_time.append(comment['snippet']['topLevelComment']['snippet']['publishedAt'])
                video_comment_parent_id.append(comment['snippet']['topLevelComment']['id'])
                video_comment_child_id.append('0') # 0 indicates this is the top-level comment
                # get replies from top comment thread
                if 'replies' in comment.keys():
                    for reply_comment in comment['replies']['comments']:
                        video_id_list.append(reply_comment['snippet']['videoId'])
                        video_comment_text.append(reply_comment['snippet']['textOriginal'])
                        video_comment_user.append(reply_comment['snippet']['authorDisplayName'])
                        video_comment_time.append(reply_comment['snippet']['publishedAt'])
                        video_comment_parent_id.append(reply_comment['snippet']['parentId'])
                        video_comment_child_id.append(reply_comment['id'])


        video_comments_dataframe = pd.DataFrame({
            'video_id':video_id_list,
            'video_comment':video_comment_text,
            'video_comment_user':video_comment_user,
            'video_comment_time':video_comment_time,
            'video_comment_parent_id':video_comment_parent_id,
            'video_comment_child_id':video_comment_child_id,
        })

        return(video_comments_dataframe)
