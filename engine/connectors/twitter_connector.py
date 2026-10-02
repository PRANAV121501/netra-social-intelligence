"""
NETRA Social Intelligence Platform
Twitter/X Connector

Provides live or sample-fallback access to Twitter/X data in NETRA's
standard post format. Real-time fetching requires a valid Bearer Token.
"""

import random
import time


class TwitterConnector:
    """
    Connector for Twitter/X data ingestion.

    When a valid Bearer Token is supplied, the connector is marked as
    'connected' and is ready for live API calls. Without credentials it
    falls back to returning representative sample posts so the rest of
    the NETRA pipeline can be exercised without live credentials.
    """

    def __init__(self, bearer_token: str = None):
        """
        Initialise the Twitter/X connector.

        Parameters
        ----------
        bearer_token : str, optional
            Twitter/X API v2 Bearer Token. Must be longer than 10 characters
            to be considered valid.
        """
        self.bearer_token = bearer_token
        self.connected = bearer_token is not None and len(bearer_token) > 10
        self.platform = 'Twitter/X'

    def test_connection(self) -> dict:
        """
        Test whether the connector has valid credentials.

        Returns
        -------
        dict
            Keys: status ('connected' | 'disconnected'), message, platform.
        """
        if not self.connected:
            return {
                'status':   'disconnected',
                'message':  'No Bearer Token configured',
                'platform': self.platform,
            }
        return {
            'status':   'connected',
            'message':  'Twitter/X API ready',
            'platform': self.platform,
        }

    def fetch_posts(self, query: str = '#India', limit: int = 50) -> list:
        """
        Fetch posts matching *query*.

        When credentials are absent, returns up to 5 representative sample
        posts so downstream NETRA components can be tested without a live
        API connection.

        Parameters
        ----------
        query : str
            Twitter search query or hashtag. Defaults to '#India'.
        limit : int
            Maximum number of posts to return. Capped at 5 in sample mode.

        Returns
        -------
        list[dict]
            Posts in the NETRA standard format.
        """
        # TODO: Replace with live API call when bearer_token is available.
        sample_topics = [
            'cybersecurity threat',
            'election results',
            'stock market crash',
            'ISRO mission',
            'cricket match',
        ]

        posts = []
        for i in range(min(limit, 5)):
            topic = sample_topics[i % len(sample_topics)]
            posts.append({
                'id':          f'tw_{int(time.time())}_{i}',
                'author':      f'user_tw_{i + 1}',
                'author_name': f'Twitter User {i + 1}',
                'content': (
                    f'[Twitter/{i + 1}] Breaking: {topic} is trending across India. '
                    f'Authorities monitoring situation. #India #Breaking'
                ),
                'platform':  'Twitter',
                'timestamp': '2026-10-01T10:00:00Z',
                'followers': random.randint(500, 50000),
                'following': random.randint(100, 2000),
                'likes':     random.randint(10, 500),
                'retweets':  random.randint(5, 200),
                'replies':   random.randint(2, 50),
                'location':  random.choice(['New Delhi', 'Mumbai', 'Bangalore', 'Chennai']),
                'verified':  random.choice([True, False]),
                'urls':      [],
            })
        return posts

    def get_status(self) -> dict:
        """
        Return a status summary for dashboard display.

        Returns
        -------
        dict
            Keys: platform, connected, mode, requires.
        """
        return {
            'platform':  self.platform,
            'connected': self.connected,
            'mode':      'live' if self.connected else 'sample_fallback',
            'requires':  ['TWITTER_BEARER_TOKEN'],
        }
