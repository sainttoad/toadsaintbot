import os
import twitter

MY_SCREEN_NAME  = 'toadsaint'

CWD             = os.path.dirname(os.path.realpath(__file__))
CSK_KEY_PATH    = os.path.join(CWD, 'csk.key')
ATS_KEY_PATH    = os.path.join(CWD, 'ats.key')

MRM_ID_PATH     = os.path.join(CWD, 'mrm.id')

class Tweeter(object):
    def __init__(self):
        consumer_key        = 'FMFDrVq0BSzgsSFBm4tZPlNoh'
        with open(CSK_KEY_PATH) as f:
            consumer_secret = f.read().strip()
        access_token_key    = '879007836314845184-XHmzNgAPbGovTdR6wiS2SL5v5PhRKgH'
        with open(ATS_KEY_PATH) as f:
            access_token_secret = f.read().strip()

        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)

        self._following_names = None

    def following_names(self, freshen_cache=False):
        if self._following_names is None or freshen_cache:
            results = self.api.GetFriends()
            self._following_names = [r.screen_name for r in results]
        return self._following_names

    def new_mentions(self):
        try:
            with open(MRM_ID_PATH) as f:
                most_recent_mention_id = f.read().strip()
        except IOError as e:
            most_recent_mention_id = None

        mentions = self.api.GetMentions(since_id=most_recent_mention_id)

        # print(mentions)
        # [Status(ID=879016054080512000, ScreenName=sainttoad, Created=Sun Jun 25 16:38:53 +0000 2017, Text=u'hola @toadsaint')]

        if mentions and len(mentions) > 0:
            with open(MRM_ID_PATH, 'w') as f:
                f.write(str(mentions[0].id))

        return mentions

    def friendly_mentions(self, require_media=False):
        friendlies = []
        for mention in self.new_mentions():
            if mention.user.screen_name in self.following_names():
                # print(mention)
                # print(dir(mention))
                # print(mention.urls)
                # print(mention.tweet_mode)
                # print(mention.source)
                # print(mention.text)
                # print(mention.media)
                # print("--------")
                if require_media is False or mention.media is not None:
                    friendlies.append(mention)

        return friendlies

if __name__ == "__main__":
    t = Tweeter()
    for mention in t.friendly_mentions(require_media=True):
        print("Retweeting: {}".format(mention))
        t.api.PostRetweet(mention.id)
    # t.api.PostUpdate("bl0rt")
    # print(t.following_names())
    # t.new_mentions()