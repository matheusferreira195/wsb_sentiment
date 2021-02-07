import praw
from textblob import TextBlob
import datetime
from models.wsb_comments import WsbComments

def wsb_get_comments(db, X, Y):
    data = db.query_wsb()

    X.append(data[0][1])
    Y.append(data[0][0])

def wsb_comment_sentiment(wsb, db):
    for comment in wsb.stream.comments():
        if comment.link_author == 'OPINION_IS_UNPOPULAR' and 'Weekend' in comment.link_title:

            analysis = TextBlob(comment.body)

            wsb_comment = WsbComments(
                comment.id,
                comment.body,
                comment.link_title,
                comment.author.name,
                comment.ups,
                0,
                analysis.polarity,
                analysis.subjectivity,
                comment.created
            )

            db.insert_wsb_comment(wsb_comment)

def create_wsb_client():
    
    client_id = 'HRP_psCzwyMwXg'
    client_secret = 'AVBYc6nLZz_R3qCcYXI_AdfZWH95Gg'
    user_agent = 'sentiment_analysis_wsb by /u/sadboy69195'

    reddit_api = praw.Reddit(client_id=client_id,
                            client_secret=client_secret,
                            user_agent=user_agent)

    wsb = reddit_api.subreddit('wallstreetbets')

    return wsb