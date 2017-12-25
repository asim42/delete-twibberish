#!/usr/bin/env python

from birdy.twitter import UserClient
import pandas as pd


def filtered_tweets(tweets, phrase):
    """Returns tweets containing `phrase`"""

    assert isinstance(tweets, pd.DataFrame)
    tweets_df = pd.DataFrame(index=tweets.index, columns=tweets.columns)
    for idx in tweets.index:
        if not isinstance(tweets.loc[idx, 'entities'], float) \
                and hasattr(tweets.loc[idx, 'entities'], 'urls'):
            urls = tweets.loc[idx, 'entities'].urls
            for url in urls:
                if phrase in url.expanded_url:
                    tweets_df.loc[idx] = tweets.loc[idx]

    tweets_df = tweets_df.dropna(axis=0, how='all')
    return tweets_df.reindex()


def main():
    """Change the value of `phrase` variable and the script will
       delete all the tweets containing it"""

    # TODO: Parameterize these
    consumer_key = 'XrPVpEA9Km1JDdpiK7sHF3Rk6'
    consumer_secret = 'kcuP7j1R0lyRMnGKwp8nzMTwiHw6kJG1k5q282NzCKaz43SiSF'
    access_token = '1099799750-ArInNlFo9zCLOMjBfgGzvvIjNwMxKV7M4QhxMix'
    access_token_secret = 'VQKRekHphQ8NYbH7D35MvZSZ3GjKaokAYwfGisPeTvLF2'
    phrase = 'fb.me'

    client = UserClient(consumer_key, consumer_secret, access_token, access_token_secret)

    resource = client.api.statuses.user_timeline

    idx = 0
    # Tweets are being retrieved here
    response = resource.get(include_rts=False, trim_user=True, exclude_replies=True, count=200)

    print('***Last Tweet***')
    print(str(response.data[0]))
    print('***Last Tweet***')
    print("Total Tweets received: " + str(len(response.data)))

    tweets = pd.DataFrame(response.data)
    tweets_df = filtered_tweets(tweets, phrase)

    while not tweets_df.index.empty:
        for idx in tweets_df.index:
            # Tweets are being deleted here
            client.api.statuses.destroy[tweets_df.loc[idx, 'id']].post()
        response = resource.get(include_rts=False, trim_user=True, exclude_replies=True, count=200,
                                since_id=tweets_df.loc[idx, 'id'])
        tweets = pd.DataFrame(response.data)
        tweets_df = filtered_tweets(tweets, phrase)
    print("Filtered Tweets: " + str(len(tweets_df.index)))


if __name__ == '__main__':
    main()
