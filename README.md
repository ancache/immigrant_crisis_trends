# migrant_crisis_trends

*An analysis of how the European refugee crisis is trending on Reddit*

*Data collection (with PRAW) and analysis (with Pandas) by [Anca Chereches](conf.ling.cornell.edu/ancache)*

*Data visualization (with D3) by Natalia Chetelat*

We're trying to understand public interest and public opinion in the European migrant crisis by analyzing Reddit activity on relevant subreddits. For now, we're focusing on [/r/europe](https://www.reddit.com/r/europe), but we hope to add other relevant subreddits to the analysis later.

The raw dataset, harvested on Sept. 21st 2015 using [grab-submissions.py](https://github.com/ancache/migrant_crisis_trends/blob/master/grab_submissions.py), contains all submissions to [/r/europe](https://www.reddit.com/r/europe) created between Jan. 1st 2015, 00:00:00 GMT and Sept. 13th 2015, 00:00:00 GMT. This dataset is available [on my website](http://conf.ling.cornell.edu/ancache/migrant_crisis) as a [Pickle file](https://docs.python.org/2/library/pickle.html). It can be loaded into Python like so:

    >>> import pickle
    >>> with ('PATH_TO_FILE/r-europe_posts.pkl','r') as f:
    >>>     posts = pickle.load(f)

`posts` is an unordered list of praw objects.

    >>> posts[0].title
    >>> u'Greeks\u2019 view of the debt crisis: \u2018What lies ahead is great, great hardship\u2019'
    >>> len(posts)
    >>> 23732


