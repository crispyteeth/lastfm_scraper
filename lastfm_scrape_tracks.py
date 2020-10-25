import requests
from bs4 import BeautifulSoup, NavigableString, Tag

'''
TODO: -- wrap this file in a method and return a collection of type 'track'
      -- new class for detailed track info (date / time listened, etc.) - make prop on 'track' class?
      -- build out the scrapers for albums and artists
      -- drill down into each track and get the date / time of when it was listened - new class
      -- build out a file and method to return csv files for each page section (albums, artists, etc.)
'''

# define user and baseUrl
user = 'chris47150'
baseUrl = f'https://www.last.fm/user/{user}/library/tracks'

# define a track
class track:
    artist = ''
    song = ''
    scrobbles = 0

    def __init__(self, artist, song, scrobbles):
        self.artist = artist
        self.song = song
        self.scrobbles = scrobbles
    
    def print_track(self):
        print(f'Artist: {self.artist} || Song: {self.song} || Scrobbles: {self.scrobbles}')

# get max pagination count
paginationResponse = requests.get(baseUrl)
paginationSoup = BeautifulSoup(paginationResponse.content, 'html.parser')
paginationItems = paginationSoup.find_all('li', class_='pagination-page')
maxPagination = 0

for paginationItem in paginationItems:
    aTag = paginationItem.findChild('a')

    if aTag:
        count = int(aTag.get_text())

        if count > maxPagination:
            maxPagination = count

# initialize collection of all tracks on page 
tracks = []

# iterate over each page and get dem tracks
for page in range(1, maxPagination + 1): 
    tracksPageUrl = f'{baseUrl}?page={page}' 
    
    # make page requests and get html
    tracksPageResponse = requests.get(tracksPageUrl)

    # get soupy
    tracksSoup = BeautifulSoup(tracksPageResponse.content, 'html.parser')

    # get all rows 
    trackRows = tracksSoup.find_all('tr', class_='chartlist-row chartlist-row--with-artist chartlist-row--with-buylinks js-focus-controls-container')

    for trackRow in trackRows:    

        artistRows = trackRow.findChild('td', class_='chartlist-artist')
        songRows = trackRow.findChild('td', class_='chartlist-name') 
        scrobbleRows = trackRow.findChild('td', class_='chartlist-bar') 

        artist = ''
        song = ''
        scrobbles = 0

        for artistRow in artistRows:            
            if isinstance(artistRow, Tag): 
                artist = artistRow.get_text()
        
                for songRow in songRows:
                    if isinstance(songRow, Tag):
                        song = songRow.get_text()                

                    for scrobbleRow in scrobbleRows:                
                        if isinstance(scrobbleRow, NavigableString): # when iterating spaces (or empty strings) are seen as type element.NavigableString
                            continue # ignore them

                        if isinstance(scrobbleRow, Tag):
                            scrobbleSpan = scrobbleRow.findChild('span', class_='chartlist-count-bar-value').get_text().strip()
                            scrobbles = int(scrobbleSpan.replace('scrobbles', '').replace('scrobble', '')) # removing the word 'scrobble(s)' and casting to int

        # add track to list and print                    
        newTrack = track(artist, song, scrobbles)
        tracks.append(newTrack)
        newTrack.print_track()





                



                


