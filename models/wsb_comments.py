from datetime import datetime
class WsbComments:
    def __init__(self, id, body, post, rddt_user, upvotes, downvotes, sentiment, subjectivity, created_at):
        self.id = id
        self.body = body.replace("'",'')
        self.post = post.replace("'",'')
        self.rddt_user = rddt_user
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.sentiment = sentiment
        self.subjectivity = subjectivity
        self.created_at = datetime.fromtimestamp(created_at)