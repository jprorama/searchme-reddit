#!/usr/bin/env python
#
# List saved r/Showerthoughts or any regex pattern match of subreddits
#
import praw
import logging
import argparse
import re
from datetime import datetime, timezone

def list_saved(listing):
    for entry in listing:
         if hasattr(entry, 'title'):
            print(entry.title)

def list_shower(listing, subreddits):
    
    pattern = '|'.join(subreddits)
        
    for entry in listing:
        if hasattr(entry, 'title'):
            title=entry.title
        else:
            title="NO TITLE"
        if hasattr(entry, 'url'):
            uri = entry.url
        else:
            uri = "https://reddit.com{}".format(entry.permalink)

        utc = datetime.fromtimestamp(entry.created_utc, timezone.utc)
            
        if re.search(pattern, entry.subreddit_name_prefixed, re.IGNORECASE):
                 print("{}|{}|{}|{}|{}|{}".format(entry.ups, entry.id, utc, entry.subreddit_name_prefixed, title, uri))

# collect list of search strings
parser = argparse.ArgumentParser(description='Filter reddit saved items by subreddit string')
parser.add_argument('-s','--subreddit', nargs='*',
                   help='case-insensitive pattern to match subreddit names')
parser.add_argument('-a', '--api',
                    help='reddit api that returns a listing of submissions')
parser.add_argument('-d', '--debug', action='store_true',
                    help='turn on debug of network connection')

args = parser.parse_args()

# work around for defining default value or empty list with the append action
# when no arguments are provided
# https://bugs.python.org/issue16399
if not args.subreddit:
    args.subreddit=['r/Showerthoughts']

# turn on connection logging
if args.debug:
    logging.basicConfig(level=logging.DEBUG)

# set up connection from praw.ini
reddit = praw.Reddit()
username = reddit.user.me()
if args.api:
    api=args.api
else:
    api="/user/{}/saved".format(username)

# query saved history
params=dict()
params['limit']=100


while True:
    saved=reddit.get(api, params)
    list_shower(saved, args.subreddit)
    if saved.after == None:
        break
    params['after'] = saved.after
