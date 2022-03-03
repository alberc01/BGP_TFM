import tweepy
from twitterDevCredentials import Credentials

class TwitterScrap():
    def __init__(self):
        cred = Credentials()
        self.__consumer_key = cred.get_consumer_api_key()
        self.__consumer_secet = cred.get_consumer_api_secret_key()
        self.__access_token = cred.get_access_token()
        self.__access_secret = cred.get_access_token_secret()
        self.__bea = cred.get_bearer_token()
        # Autenticacion en Twitter
        self.__auth = tweepy.OAuthHandler(self.__consumer_key, self.__consumer_secet)
        self.__auth.set_access_token(self.__access_token ,self.__access_secret)
        # Obtener el objeto API
        self.__api = tweepy.API(self.__auth, wait_on_rate_limit= True)
        try:
            self.__api.verify_credentials()
            self.__client = tweepy.Client(self.__bea,wait_on_rate_limit= True)
        except:
            print("Error durante la autenticacion")

    def get_number_of_tweets(self, username):
        user = self.__api.get_user(screen_name = username)
        return user.statuses_count


    def scrap_info_by_user(self, username):
        return tweepy.Cursor(self.__api.user_timeline, screen_name=username).items()

    def scrap_info_by_user_between_dates(self, username, since_id):
        return tweepy.Cursor(self.__api.user_timeline, screen_name=username, since_id = since_id ).items()
    
