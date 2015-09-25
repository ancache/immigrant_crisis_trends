import pandas as pd
from pandas import DataFrame
import numpy as np

def get_num_refugee_posts(posts):
	
	posts['month'] = posts.index.to_period('M')
	counts_by_topic = posts.groupby(['month','topic']).size()
	counts_by_topic_df = counts_by_topic.unstack()
	counts_by_topic_df['%refugee'] = counts_by_topic_df['refugee'] / \
		(counts_by_topic_df['refugee'] + counts_by_topic_df['not refugee'])
	avg_refugee_posts_precrisis = np.mean(counts_by_topic_df.loc[:'2015-03','%refugee'])
	counts_by_topic_df['refugee_expected'] = np.floor(
		avg_refugee_posts_precrisis * counts_by_topic_df['not refugee'])
	to_export = counts_by_topic_df.drop(['not refugee','%refugee'],axis=1)
	
	to_export.to_csv("total_num_posts.csv")

if __name__ == '__main__':

	posts = pd.read_pickle("r-europe_posts_frame.pkl")	

	get_num_refugee_posts(posts)