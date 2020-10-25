import requests
import lastfm_pagination as lastfm
from bs4 import BeautifulSoup, NavigableString, Tag

# define an album
class album:
    artist = ''
    name = ''
    scrobbles = 0

    def __init__(self, artist, album, scrobbles):
        self.artist = artist
        self.name = album
        self.scrobbles = scrobbles
    
    def print_album(self):
        print(f'Artist: {self.artist} || Album: {self.name} || Scrobbles: {self.scrobbles}')

# provide username and # of pages (not required - will default to max)
def getAlbums(user, maxPagination=None):

    # define baseUrl
    baseUrl = f'https://www.last.fm/user/{user}/library/albums'

    # get max pagination count
    if maxPagination is None:
        maxPagination = lastfm.getMaxPagination(baseUrl)

    # initialize collection of all albums on page
    albums = []

    # iterate over each page and get dem albums
    for page in range(1, maxPagination + 1):
        albumsPageUrl = f'{baseUrl}?page={page}'

        # make page requests and get response
        albumsPageResponse = requests.get(albumsPageUrl)

        # get soupy
        albumsSoup = BeautifulSoup(albumsPageResponse.content, 'html.parser')

        # get all rows 
        albumRows = albumsSoup.find_all('tr', class_='chartlist-row chartlist-row--with-artist chartlist-row--with-buylinks js-focus-controls-container link-block-basic js-link-block')
        
        for albumRow in albumRows:

            artistRows = albumRow.findChild('td', class_='chartlist-artist')
            albumRows = albumRow.findChild('td', class_='chartlist-name')
            scrobbleRows = albumRow.findChild('td', class_='chartlist-bar')

            artist = ''
            albumName = ''
            scrobbles = 0

            for artistRow in artistRows:
                if isinstance(artistRow, Tag):
                    artist = artistRow.get_text()
                    
                    for albumRow in albumRows:
                        if isinstance(albumRow, Tag):
                            albumName = albumRow.get_text()
                            
                        for scrobbleRow in scrobbleRows:
                            if isinstance(scrobbleRow, NavigableString): # when iterating spaces (or empty strings) are seen as type element.NavigableString
                                continue # ignore them

                            if isinstance(scrobbleRow, Tag):
                                scrobbleSpan = scrobbleRow.findChild('span', class_='chartlist-count-bar-value').get_text().strip()
                                scrobbles = int(scrobbleSpan.replace('scrobbles', '').replace('scrobble', '')) # removing the word 'scrobble(s)' and casting to int                                    

            # add album to list
            newAlbum = album(artist, albumName, scrobbles)
            albums.append(newAlbum)

    return albums