'''
Tutorial(s):
-https://www.geeksforgeeks.org/python-web-scraping-tutorial/
-https://oxylabs.io/blog/python-web-scraping

Creating a webscraping tool to make a phone call to myself when the below bikes are in inventory
https://www.canyon.com/en-us/road-bikes/race-bikes/ultimate/cf-sl/ultimate-cf-sl-8-disc/3073.html?dwvar_3073_pv_rahmenfarbe=GY%2FBK
https://www.canyon.com/en-us/road-bikes/race-bikes/ultimate/cf-sl/ultimate-cf-sl-8-disc-di2/3075.html?dwvar_3075_pv_rahmenfarbe=GY%2FBK

Application workflow - 

1)  Check to see if there is any bikes in stock for specific size/model using scraper
2)  If there is, create API request to Twilio confirming if there has been a call created in the past 24 hours to notify.
    Create call to notify customer that the bike is available
3)  Create message with link to webpage of available bike along with sizing information, etc.
'''
import requests,bikes,functions
from bs4 import BeautifulSoup

#Creating an array of URLs that need to be scraped, then create an array of bike objects
bike_list = functions.create_bikes()
print(bike_list[0].model_url)