from twilio.rest import Client
from corgiTexter.models import Post
import random
from sqlalchemy.sql import func
import os

## Twilio API Connection
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
client = Client(account_sid, auth_token)


def factPuller():
    fact_random = Post.query.order_by(func.random()).first()
    factFact = fact_random.fact
    factSource = fact_random.source
    return factFact, factSource