import requests 
from bs4 import BeautifulSoup

def getMaxPagination(baseUrl):
    
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

    return maxPagination