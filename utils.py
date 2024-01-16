def search_youtube(youtube, search_query):
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        maxResults=10,
        type="video"
    )
    return request.execute()