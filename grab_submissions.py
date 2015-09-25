import praw
import time
import cPickle as pickle
import ipdb
import sys

USER_AGENT = "MacOS: Refugee crisis-related activity monitor by /u/lapropriu:v1.0"

# --> note: submission timestamps are actually in GMT-8
START_TIME = 1420099200  # Jan. 1st 2015, 08:00:00 GMT 
#START_TIME = 1439424000 # Thu, 13 Aug 2015 00:00:00 GMT --> for TESTING purposes
END_TIME = 1442131200 # Sept. 13th 2015, 08:00:00 GMT
INTERVAL = 259200 # 3 days

WAIT = 20 # for building in a delay between Reddit API requests (max is 30/min)
MAX_POSTS = 1000 # maximum number of posts Reddit will return in a search


class Timer(object):
    '''Class that can be used measure timing using system clock'''
    def __init__(self, name = None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        sys.stdout.write('-> %s [elapsed: %.2f s]\n' % (self.name, time.time() - self.tstart))

def pprint_unix_time(unix_time):
	
	return time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(unix_time))


def search_sub(reddit, query, sub):

	return list(r.search(query, subreddit=sub, sort='new', limit=None, syntax='cloudsearch'))
	
def repeat_search(reddit):
	posts = []; l = []
	timestamp = START_TIME
	
	while timestamp < END_TIME:
		try:
			query = "timestamp:{0}..{1}".format(timestamp, timestamp+INTERVAL)
			l = search_sub(r, query, 'europe')
			posts = posts + l
			if len(l) > 0.9*MAX_POSTS:
				print("\tWARNING! Getting close to Reddit's search results limit." +
					" There might be more posts in this timeframe which we failed to retrieve.")									
			#ipdb.set_trace()
			
		except Exception as e:
			print("An error has occurred for search starting at " + 
				pprint_unix_time(timestamp) + ":\n" + str(e))

		else:
			print("Done for " + pprint_unix_time(timestamp) + 
				". Found {} posts.".format(len(l)))
			timestamp = timestamp + INTERVAL
		print("     Timestamp is now {}.".format(timestamp))					

		time.sleep(WAIT)

	return posts
	

if __name__ == '__main__':

	with Timer('Getting Reddit submissions: '):
		r = praw.Reddit(USER_AGENT)
		posts = repeat_search(r)
	
	# remove duplicates; note: order is not preserved
	posts = list(set(posts))
	
	with Timer('Saving submissions to file: '):
		with open("r-europe_posts.pkl", 'wb') as f:
			pickle.dump(posts, f)
	
	sys.stdout.write('DONE!')
	
			
