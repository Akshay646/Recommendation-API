import requests;

class Locations:
    @staticmethod
    def get_user_country():
    # Get the user's IP address information
        response = requests.get('https://ipinfo.io')
        data = response.json()
    
        # Extract the country information
        country = data.get('country')
        return country


