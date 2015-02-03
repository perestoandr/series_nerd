import time
from apps.main import controllers

def cron():
    controllers.twit()

cron()
