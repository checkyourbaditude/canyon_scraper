'''
Tutorial(s):
-https://www.geeksforgeeks.org/python-web-scraping-tutorial/
-https://oxylabs.io/blog/python-web-scraping

Creating a webscraping tool to make a phone call to myself when the below bikes are in inventory
https://www.canyon.com/en-us/road-bikes/race-bikes/ultimate/cf-sl/ultimate-cf-sl-8-disc/3073.html?dwvar_3073_pv_rahmenfarbe=GY%2FBK
https://www.canyon.com/en-us/road-bikes/race-bikes/ultimate/cf-sl/ultimate-cf-sl-8-disc-di2/3075.html?dwvar_3075_pv_rahmenfarbe=GY%2FBK

Call workflow with twilio
https://www.twilio.com/docs/voice/tutorials/how-to-retrieve-call-logs-python

Application workflow - 

1)  Check to see if there is any bikes in stock for specific size/model using scraper
2)  If there is, create API request to Twilio confirming if there has been a call created in the past 24 hours to notify.
    Create call to notify customer that the bike is available
3)  Create message with link to webpage of available bike along with sizing information, etc.
'''
import requests, os, functions, bikes
from bs4 import BeautifulSoup
from twilio.rest import Client
from datetime import datetime, timedelta

def make_get_request(url_list):
    try:
        r = requests.get(url_list)
        print(f"Status Code: ", r.status_code)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    # Finding by id
    s = soup.find('div', class_='productConfiguration js-productConfiguration xlt-pdpVariations')

    return s

def get_sizes(size_html):
    sizes_list = {}
    
    for element in size_html.find_all('li'):
        #Find the bike size information
        find_size = element.find("div", class_='productConfiguration__variantType js-productConfigurationVariantType')
        size_avail = None

        #Collect the sizes from the page
        try:
            size = find_size.text.strip()
        except AttributeError:
            print("Found attribute error when scraping the size element: "+str(size))
            continue

        #Find if the bike is in stock
        if element.find('button', class_='productConfiguration__selectVariant productConfiguration__selectVariant--button js-productConfigurationSelect'):
            size_avail = True
        elif element.find('button', class_='button button--secondary button--rounded productConfiguration__notificationButton productConfiguration__notificationButton--hasIcon js-notifyMeModalTrigger'):
            size_avail = False

        sizes_list.update({size:size_avail})

    print(sizes_list)

    #return the final availability list
    return sizes_list

def create_correspondence(size_avail, bike_url,client_creds):
    is_size_avail = False

    for x in size_avail:
        if x == 'L' and size_avail[x] == True:

            #generate a call and message if a call has not been answered in the past 8 hours
            is_size_avail = True

            if is_size_avail == True:
                sms_body = "Your Canyon Bike is available at "+bike_url
                message = client_creds.messages.create(
                        body=sms_body,
                        from_='+18187226781',
                        to='+18184899279'
                    )
                print(message.sid)
    
    return is_size_avail

def check_last_call(client_creds):
    calls = client_creds.calls.list(to='+18184899279', limit=100)
    for record in calls:
        current_datetime = datetime.now()
        #print("Current date: "+current_datetime.strftime("%c"))
        current_datetime -= timedelta(hours = 8)
        #print("Current date - 8: "+current_datetime.strftime("%c"))
        #print("Call End Time: "+str(record.end_time))
        #print("Is now greater than the call time? "+ str(current_datetime.timestamp() > record.end_time.timestamp()))
        if (record.status == 'completed' and not (current_datetime.timestamp() > record.end_time.timestamp())):
            print("Previous call detected with SID of:"+record.sid)
            return True
    
    print("No previous calls detected in the past 8 hours.")
    return False

#Twilio Credentials
account_sid = str(os.environ['TWILIO_ACCOUNT_SID'])
auth_token = str(os.environ['TWILIO_AUTH_TOKEN'])
client = Client(account_sid, auth_token)
create_call = False

#Check if call was made before doing anything
if not check_last_call(client):

    #Get all of the bike URLs for processing
    bike_url_list = functions.get_URLs()

    #loop through the bikes list, get the inventory, then create correspondence accordingly
    for bike in bike_url_list:

        parsed_html = make_get_request(bike)
        sizes_dictionary = get_sizes(parsed_html)

         #Check if messages should be sent for the bike, then update the create_call parameter if this is completed
        if create_correspondence(sizes_dictionary,bike,client):
            create_call = True

    #Create call if needed
    if create_call:
        call = client.calls.create(
            url='http://demo.twilio.com/docs/voice.xml',
            to='+18184899279',
            from_='+18187226781'
        )
        print(call.sid)