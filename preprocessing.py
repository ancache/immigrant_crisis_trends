import cPickle as pickle
from pandas import DataFrame
import pandas as pd
import numpy as np
import re
from grab_submissions import pprint_unix_time

def DataFrame_from_PRAW(posts_l):
	
	# sort by timestamp
	timestamp = [p.created for p in posts_l]
	sorted_timestamp_ix = np.argsort(timestamp)
	posts_l = np.array(posts_l)[sorted_timestamp_ix].tolist()
	timestamps = [pd.to_datetime(post.created, unit='s') for post in posts_l]
	
	# create dataframe
	posts = DataFrame({},index=timestamps)	
	posts['title'] = [p.title for p in posts_l]
	posts['selftext'] = [p.selftext for p in posts_l]	
	posts['url'] = [p.url for p in posts_l]
	posts['domain'] = [p.domain for p in posts_l]	
	posts['author'] = [p.author for p in posts_l]
	posts['author_flair'] = [p.author_flair_text for p in posts_l]			
	posts['score'] = [p.score for p in posts_l]
	posts['ups'] = [p.ups for p in posts_l]
	posts['downs'] = [p.downs for p in posts_l]	
	posts['gilded'] = [p.gilded for p in posts_l]
	posts['permalink'] = [p.permalink for p in posts_l]
	posts['redditID'] = [p.fullname for p in posts_l]
	posts['link_flair_text'] = [p.link_flair_text for p in posts_l]
	
	# NOTE: this should not be necessary after re-running the crawler 
	# at this point, it is removing posts from 2014, which should not have been retrieved
	posts = posts['2015']

	return posts
	
def index_refugee_posts(posts):
	
	posts['refugee_in_title'] = [False] * len(posts)
	posts['refugee_in_text'] = [False] * len(posts)
	query = "(immigrant)|(migrant)|(refugee)|(asylum seeker)"
	
	for i in range(len(posts)):
		if re.search(query, posts['title'][i]):
			posts['refugee_in_title'][i] = True
		if re.search(query, posts['selftext'][i]):
			posts['refugee_in_text'][i] = True
			
	return posts


if __name__ == '__main__':

	with open('r-europe_posts.pkl','rb') as f:
		posts_l = pickle.load(f)

	# create data frame from raw data	
	posts = DataFrame_from_PRAW(posts_l)

	# index refugee-related posts
	posts = index_refugee_posts(posts)
	
	# save to file
	posts.to_pickle("posts-r-europe.pickle")
	