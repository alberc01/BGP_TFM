from cmath import sin
from importlib import import_module
from twitter_class import TwitterScrap
from gDrive_class import GoogleDriveApi
from writer_class import Writer
from parser_class import Parser
import os
import json
import datetime
import iso8601

class Main():

    def __init__(self):
        self.scrapp = TwitterScrap()
        self.parser = Parser()
        self.writer = Writer()
        self.gdrive = GoogleDriveApi()
    
    def store_inital_data(self):
        dic_info = {}
        user_tweets = self.scrapp.scrap_info_by_user("bgpstream")
        dic_info, last_date = self.parser.get_bgp_info_of_tweets(dic_info, user_tweets)

        f_name = str(last_date)+".json"
        self.writer.write_dict_to_file(f_name, dic_info)
 
        list_of_files = [f_name]
        self.gdrive.upload_files(list_of_files,'1lLBCk9CxaCKLyOb8Wwagge05t6f-yNRc')
        print("------------------------------Data saved------------------------------")

        os.remove(f_name)
    
    def fix_dictionary_date(self):
        file, content = self.gdrive.download_file('1lLBCk9CxaCKLyOb8Wwagge05t6f-yNRc')
        dict_data = json.loads(content)
        firstIter = True
        mindate = 0
        res = 0
        for k,v in dict_data.items():
            if k not in ['recent_date', 'last_date', 'max_id']:
                for item in v:
                    date_in_dict = datetime.datetime.strptime(item['raw']['date'], '%Y-%m-%d %H:%M:%S%z')
                    if firstIter:
                        firstIter = False
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']
                    elif date_in_dict > res:
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']

        dict_data["recent_date"] = str(res).lstrip(' ')
        dict_data["max_id"] = max_id
        self.gdrive.update_gdrive_file(file, json.dumps(dict_data,indent=4))
        print("------------------------------Data updated------------------------------")

    def update_dictionary_dates(self, dict_info):
        firstIter = True
        mindate = 0
        res = 0
        for k,v in dict_info.items():
            if k not in ['recent_date', 'last_date', 'max_id']:
                for item in v:
                    date_in_dict = datetime.datetime.strptime(item['raw']['date'], '%Y-%m-%d %H:%M:%S%z')
                    if firstIter:
                        firstIter = False
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']
                    elif date_in_dict > res:
                        res = date_in_dict
                        max_id = item['raw']['tweet_id']

        dict_info["recent_date"] = str(res).lstrip(' ')
        dict_info["max_id"] = max_id

        return dict_info



    def update_data(self):
        
        file, content = self.gdrive.download_file('1lLBCk9CxaCKLyOb8Wwagge05t6f-yNRc')
        dict_data = json.loads(content)
        since_id = int(dict_data['max_id'])

        user_tweets =  self.scrapp.scrap_info_by_user_between_dates(username="bgpstream",since_id=since_id)

        dic_info, last_date = self.parser.get_bgp_info_of_tweets(dict_data, user_tweets)
        
        dic_info = self.update_dictionary_dates(dic_info)

        self.gdrive.update_gdrive_file(file, json.dumps(dic_info,indent=4))
        print("------------------------------Data updated------------------------------")
              
        return dict_data


# Main().fix_dictionary_date()

# Main().store_inital_data()
Main().update_data()