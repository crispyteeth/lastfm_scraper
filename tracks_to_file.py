import lastfm_scrape_tracks as lastfm
from datetime import datetime
import argparse
import csv

# sets up arguments - pass in user and maxPages (optional)
parser = argparse.ArgumentParser()
parser.add_argument('user', help='the lastfm user to search')
parser.add_argument('maxPages', nargs='?', type=int, default=None, help='number of pagination pages to scrape')
args = parser.parse_args()

# create a pipe delimited file - could do csv but cleanup may be messy?
with open(f'tracks_{args.user}_{datetime.now()}.txt', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')

    writer.writerow(['Artist', 'Track', 'Scrobbles'])

    tracks = lastfm.getTracks(args.user, args.maxPages)
    for track in tracks:
        writer.writerow([track.artist, track.name, track.scrobbles])