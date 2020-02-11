#!/usr/bin/env python
# coding: utf-8

# In[54]:


# Weather check
# Bus check
# books check
# reminders/alerts


# In[55]:


from pprint import pprint
import requests
import re
import time
from datetime import datetime
import threading 


# In[56]:


# using openweathermap
# api.openweathermap.org/data/2.5/weather?q={city name},{state},{country code}&appid={your api key}
# api.openweathermap.org/data/2.5/weather?zip=94040,us&appid={your api key}
class Weather:
    def __init__(self):
        # use your own API keys
        self.fetched = False
        f = open("./../weatherApiKeys.txt", "r")
        self.apikey = f.read().strip()
        print("->  Getting Weather info...")
        self.req_today_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=94132,us&appid=' + self.apikey)
        if(self.req_today_weather.status_code == 200):
            self.fetched = True
            print("->  Fetched successfully!")
            self.json_today_weather = self.req_today_weather.json()
            #         extracting and setting other variables
            self.temp_min = (self.json_today_weather["main"]["temp_min"] - 273.15) * 9/5 + 32
            self.temp_max = (self.json_today_weather["main"]["temp_max"] - 273.15) * 9/5 + 32
#             kelvin to F
            self.description = self.json_today_weather["weather"][0]["description"]
            self.visibility = self.json_today_weather["visibility"] * 0.000621371 # in miles
            self.wind = self.json_today_weather["wind"]["speed"] * 2.23694 # in miles/hr
            
        else:
            print("->  Unsuccessful Fetch!")
        
        
        

        
    def isFetched(self):
        return self.fetched
    def isWindy(self):
        if(self.wind > 13):
            return 1.0
        elif(self.wind > 9 and self.wind <= 13):
            return 0.5
        else:
            return 0
        def isFog(self):
            if(selfvisibility <= 7):
                return 1
            elif(selfvisibility <= 9 and selfvisibility > 7):
                return 0.5
            else:
                return 0
    def isCold(self):
        if(self.temp_max < 53 or self.temp_min <53):
            return 1
        else:
            return 0
    def getDescription(self):
        return self.description
    


# In[ ]:





# In[57]:


# bus
# sf-muni
# 57
# 4704

# list of agencies:
# http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList
# list of lines:
# http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=sf-muni
# list of stops:
# http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r=57
# predictions at a stop:
# http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=57&s=4704


# In[58]:


class busSchedule():
    def getPrediction(self):
        req_BS = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=57&s=4704')
        if(req_BS.status_code == 200):
            print("->  Fetched Schedule!")
            text = req_BS.text
            startList = ([m.start() for m in re.finditer('<prediction ', text)])
            endList = ([m.start() for m in re.finditer('/>', text)])
            predictionList = []
            for i in range(len(startList)):
                listele = text[startList[i]:endList[i]]
                predictionList.append(listele[listele.find("minutes"):listele.find("isDeparture")].strip()[9:-1]) 
            return(predictionList)
        else:
            print("->  Error occured while fetching Bus prediction")
            return None


# In[59]:


def PRINTTIME():
    while(True):
        print("->  Time: " + str(datetime.now()).split(" ")[1].split(".")[0])
        time.sleep(60)


# In[60]:


def DAILYSCHEDULE():
    weatherToday = Weather()
    scheduleToday = busSchedule()
    if(weatherToday.isFetched): 
        print("->  Weather today:")
        print("->     isWindy: " + str(weatherToday.isWindy()))
        print("->     isCold: " + str(weatherToday.isCold()))
        print("->     getDescription: " + str(weatherToday.getDescription()))
        print()
    while(True):
        schedule = scheduleToday.getPrediction()
        if(schedule is not None):
            print("->  Next Buses in: ",end="" )
            print(schedule)
            print()
            time.sleep(60*3)


# In[ ]:





# In[53]:


if(__name__ == "__main__"):    
    t1 = threading.Thread(target = DAILYSCHEDULE)
    t2 = threading.Thread(target = PRINTTIME)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    while True:
        pass


# In[ ]:




