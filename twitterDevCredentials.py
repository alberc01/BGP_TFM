
class Credentials:
    def __init__(self):
        self.consumer_api = "YOUR_TWITTER_CONSUMER_KEY"
        self.consumer_secret = "YOUR_TWITTER_CONSUMER_SECRET_KEY"
        self.bearer = "YOUR_TWITTER_BEARER_TOKEN"
        self.access = "YOUR_TWITTER_ACCESS_KEY"
        self. access_secret = "YOUR_TWITTER_ACCESS_SECRET_KEY"

    def get_consumer_api_key(self):
        return self.consumer_api

    def get_consumer_api_secret_key(self):
        return self.consumer_secret

    def get_bearer_token(self):
        return self.bearer

    def get_access_token(self):
        return self.access

    def get_access_token_secret(self):
        return self.access_secret