import praw
from textblob import TextBlob
import datetime

def wsb_comment_sentiment(wsb, X,Y):
    for comment in wsb.stream.comments():
        if comment.link_author == 'AutoModerator' and 'Daily' in comment.link_title:

            analysis = TextBlob(comment.body)

            y_vec = analysis.sentiment.polarity
            x_vec = datetime.datetime.now()

            Y.append(y_vec)
            X.append(x_vec)

            #break

def create_wsb_client():
    
    client_id = 'HRP_psCzwyMwXg'
    client_secret = 'AVBYc6nLZz_R3qCcYXI_AdfZWH95Gg'
    user_agent = 'sentiment_analysis_wsb by /u/sadboy69195'

    reddit_api = praw.Reddit(client_id=client_id,
                            client_secret=client_secret,
                            user_agent=user_agent)

    wsb = reddit_api.subreddit('wallstreetbets')

    return wsb