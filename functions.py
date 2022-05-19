import bikes,requests,csv
from bs4 import BeautifulSoup

#creates a list of blank bike objects with URL list
def create_bikes():
    url_list = get_URLs()
    bike_list = []

    for bike_url in url_list:
        temp_bike = bikes.bike()
        temp_bike.model_url = bike_url
        temp_bike.model_name = get_model(bike_url)
        bike_list.append(temp_bike)

    return bike_list

#returns the model number of the URL provided
def get_model(url):
    try:
        r = requests.get(url)
        print(f"Status Code: ", r.status_code)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)

    soup = BeautifulSoup(r.content, 'html.parser')
    model_name = soup.find("h1", class_='heading heading--2 productDescription__productName xlt-pdpName')
    return model_name.text.strip()

#This function grabs a list of URLs from the 'canyon_URLs.txt' file
def get_URLs():
    with open('canyon_URLs.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        list_of_rows = list(csv_reader)
        urls_final = list_of_rows[0]
    
    return urls_final

def print_bikes(bike_list):
    for attr, value in bikes.__dict__.items():
        print(attr, value)