import requests

def search_youtube(youtube, search_query):
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        maxResults=10,
        type="video"
    )
    return request.execute()

def get_current_ip():
    try:
        response = requests.get('http://api.ipify.org')
        if response.status_code == 200:
            return response.text  # Returns the IP address as a string
        else:
            return "Error: Unable to fetch IP address"
    except requests.RequestException:
        return "Error: Request failed"