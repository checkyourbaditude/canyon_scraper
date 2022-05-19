'''
This is the bike class to hold all of the data during the scraping process
'''

class bike:
    #constructor for creating blank object
    def __init__(self):
        self.model_name = ''
        self.model_url = ''
        self.model_inventory = {
            "2XS":"None",
            "XS":"None",
            "S":"None",
            "M":"None",
            "L":"None",
            "XL":"None",
            "2XL":"None"
        }

    #Create class methods here
    