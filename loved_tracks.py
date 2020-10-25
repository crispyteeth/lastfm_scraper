import lastfm_pagination as lastfm
from bs4 import BeautifulSoup, Tag
import requests

# define loved track
class lovedTrack:
    artist = ''
    song = ''

    def __init__(self, artist, song):
        self.artist = artist
        self.song = song

    def print_loved_track(self):
        print(f'Artist: {self.artist} || Song: {self.song}')

# provide user and # of pages (not required - will default to max)
def getLovedTracks(user, maxPagination=None):

    # define baseUrl
    baseUrl = f'https://www.last.fm/user/{user}/loved'

    # get max pagination count
    if maxPagination is None:
        maxPagination = lastfm.getMaxPagination(baseUrl)
    
    lovedTracks = []

    for page in range(1, maxPagination + 1):
        lovedTracksPage = f'{baseUrl}?page={page}'
        lovedTracksResponse = requests.get(lovedTracksPage)
        lovedTracksSoup = BeautifulSoup(lovedTracksResponse.content, 'html.parser')
        lovedTracksRows = lovedTracksSoup.find_all('tr', class_='chartlist-row chartlist-row--with-artist chartlist-row--with-buylinks js-focus-controls-container')

        for lovedTrackRow in lovedTracksRows:
            artistRows = lovedTrackRow.findChild('td', class_='chartlist-artist')
            songRows = lovedTrackRow.findChild('td', class_='chartlist-name')

            artist = ''
            song = ''

            for artistRow in artistRows:            
                if isinstance(artistRow, Tag): 
                    artist = artistRow.get_text()
            
                    for songRow in songRows:
                        if isinstance(songRow, Tag):
                            song = songRow.get_text()                

            newLovedTrack = lovedTrack(artist, song)
            lovedTracks.append(newLovedTrack)
    
    return lovedTracks