from twilio.rest import Client
from core.models import Post
import random
from sqlalchemy.sql import func
import os


client = Client(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])


def factPuller():
    fact_random = Post.query.order_by(func.random()).first()
    factFact = fact_random.fact
    factSource = fact_random.source
    return factFact, factSource