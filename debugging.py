from apps.wsb import *
from collections import deque

wsb = create_wsb_client()
X = deque(maxlen=20)
Y = deque(maxlen=20)

wsb_comment_sentiment(wsb, X, Y)