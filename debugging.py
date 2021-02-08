from apps.gme_data import *
from collections import deque

X = deque(maxlen=20)
Y = deque(maxlen=20)

gme_stock_price()