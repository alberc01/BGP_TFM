class Parser():
    # Funcion para clasificar el tipo de tramas publicadas en twitter de caracter BGP
    def get_bgp_info_of_tweets(self,dic_info, user_tweets):
        cont = 0

        for tweet in user_tweets:
            print(str(tweet.created_at).lstrip(' '))
            frame = tweet.text.replace("-","").replace(u'\u2026', ",").split(',')
            protocol = str(frame[0]).lstrip(' ')
            issue = str(frame[1]).lstrip(' ')
            url = str(frame[-1]).lstrip(' ')
            tweet_id = str(tweet.id)
            last_date = str(tweet.created_at).lstrip(' ')

            if not cont:
                dic_info["recent_date"] =  str(tweet.created_at).lstrip(' ')
                dic_info["max_id"] = tweet_id
                cont+=1

            if issue == "HJ":
                injured_end = frame.index('',2,-1)
                injured_info = frame[2:injured_end]
                causer_info = frame[injured_end+1:-1]

                injured_dic = {
                    "issue":str(injured_info[0]).lstrip(' '),
                    "company":str(",".join(injured_info[1:-1])).lstrip(' '),
                    "country":str(injured_info[-1]).lstrip(' '),
                    "url": url
                }

                causer_dict = {
                    "company":str(causer_info[0]).lstrip(' '),
                    "country":str(causer_info[-1]).lstrip(' '),
                    "url": url
                }

                if issue in dic_info:
                    dic_info[issue].append({
                        "protocol": protocol,
                        "injured":injured_dic,
                        "causer":causer_dict,
                        "raw": {
                            "text":tweet.text,
                            "date": str(tweet.created_at).lstrip(' '),
                            "tweet_id":tweet_id
                            }
                    })
                else:
                    dic_info[issue] = [{
                        "protocol": protocol,
                        "injured":injured_dic,
                        "causer":causer_dict,
                        "raw": {
                            "text":tweet.text,
                            "date":str(tweet.created_at).lstrip(' '),
                            "tweet_id":tweet_id
                        }
                    }]
            elif issue == "OT":
                try:
                    outage_end = frame.index('',2,-1)
                except:
                    outage_end = len(frame)-1
                outage_info = frame[2:outage_end]
                prefix_affected = frame[outage_end+1:-1]

                outage_dic = {
                    "id":str(outage_info[0]).lstrip(' '),
                    "company":str(",".join(outage_info[1:-1])).lstrip(' ') ,
                    "country":str(frame[outage_end-1]).lstrip(' '),
                    "prefix_affected": str(",". join(prefix_affected)).lstrip(' '),
                    "url":url,
                    "raw": {
                        "text":tweet.text,
                        "date":str(tweet.created_at).lstrip(' '),
                        "tweet_id":tweet_id                    
                    }
                }
                
                if issue in dic_info:
                    dic_info[issue].append(outage_dic)
                else:
                    dic_info[issue] = [outage_dic]
                
            dic_info["last_date"] = last_date

        return dic_info, dic_info["last_date"]




