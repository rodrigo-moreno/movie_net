import requests
from bs4 import BeautifulSoup
import csv
import re
from numpy import nan

class _ActorOption():
    '''
    A precise object to represent an Actor Option in a search.
    '''
    def __init__(self, soup):
        self.soup = soup
        self._get_name()
        self._get_code()

    def __repr__(self):
        return f'{self.name}: {self.code}'

    def __str__(self):
        return f'{self.name}: {self.code}'

    def _get_name(self):
        self.name = self.soup.find_all('a')[-2].text

    def _get_code(self):
        href = self.soup.find('a')
        href = href.attrs['href']
        self.code = href.split('/')[2]


class _MovieOption():
    '''
    A precise object to represent a Movie Option in a search.
    '''
    def __init__(self, soup):
        self.soup = soup
        self._get_name()
        self._get_code()
        self._get_year()

    def __repr__(self):
        return f'{self.name} ({self.year}): {self.code}' 

    def __str__(self):
        return f'{self.name} ({self.year}): {self.code}'

    def _get_name(self):
        self.name = self.soup.find_all('a')[-1].text

    def _get_code(self):
        href = self.soup.find('a')
        href = href.attrs['href']
        self.code = href.split('/')[2]

    def _get_year(self):
        text = self.soup.text.strip()
        try:
            re_match = re.search('\((\d*)\)', text)
            self.year = re_match.group(1)
        except:
            self.year = nan


class Option():
    '''
    An object to represent a single option from IMDB search.
    '''
    def __init__(self, soup, type_):
        self.soup = soup
        self.type = type_
        if self.type == 'movie':
            self.option = _MovieOption(self.soup)
        elif self.type == 'actor':
            self.option = _ActorOption(self.soup)

    def __repr__(self):
        return str(self.option)

    def __str__(self):
        return str(self.option)



class Options():
    '''
    An object...
    '''
    def __init__(self, options, type_):
        self.options = [Option(soup, type_) for soup in options]
        self.positions = [ii + 1 for ii in range(len(self.options)]

    def __repr__(self):
        out = f'List of {len(self.options)} options\n'
        for pos, option in enumerate(self.options):
            out += f'[{pos + 1}] {option}\n\n'
        return out

    def __str__(self):
        out = f'List of {len(self.options)} options\n'
        for pos, option in enumerate(self.options):
            out += f'[{pos + 1}] {option}\n\n'
        return out

    def display(self, start, n):
        '''
        A method to display n choices, starting from the one specified in
        start.

        Input:
        - start: index of the first to display.
        - n: the amount of choices to display.

        Output:
        - none
        '''
        pass


class Search():
    '''
    An object to represent a search result from IMDB.
    '''
    def __init__(self, keywords, type_):
        self.keywords = keywords
        self.type = type_
        if self.type == 'movie':
            url = 'https://www.imdb.com/find?s=tt&q={}&ref_=nv_sr_sm'
        elif self.type == 'actor':
            url = 'https://www.imdb.com/find?s=nm&q={}&ref_=nv_sr_sm'
        self.url = url.format(self.keywords)

    def __repr__(self):
        return (f'Search object with keywords: {self.keywords}\n'
                f'                       type: {self.type}')

    def __str__(self):
        return (f'Search object with keywords: {self.keywords}\n'
                f'                       type: {self.type}')

    def _find_movies(self):
        slist = self.soup.find_all(class_ = 'findSection')
        section_name = 'Titles'
        for section in slist:
            title = section.find(class_ = 'findSectionHeader').text
            if title == section_name:
                self.options = section.find_all('tr')
                break

    def _find_actors(self):
        slist = self.soup.find_all(class_ = 'findSection')
        section_name = 'Names'
        for section in slist:
            title = section.find(class_ = 'findSectionHeader').text
            if title == section_name:
                self.options = section.find_all('tr')
                break

    def find(self):
        if self.type == 'movie':
            self._find_movies()
        elif self.type == 'actor':
            self._find_actors()
        else:
            err_msg = 'Object type does not match any of the search types.'
            raise TypeError(err_msg)

    def search(self):
        header = {'Accept-Language': 'en-US'}
        self.resp = requests.get(self.url, headers = header)
        self.soup = BeautifulSoup(self.resp.content, 'html.parser')
        self.find()
        self.options = Options(self.options, self.type)

    def choose(self):
        found = False
        rounds = 0
        while not found:
            self.options.display(start = rounds * 5, 5)
            selection = input()
            if selection.isnumeric():
                found = True
                return self.options.options[selection - 1]
            else:
                rounds += 1





################################################################################
################################################################################
################################################################################
### GET DATA FROM HISTORY FILE
def main():
    movies = []
    actors = []
    with open('history.csv', 'r') as f:
        for line in csv.reader(f):
            movies.append(line[0])
            actors.append(line[1])
    
    #search = input('Enter movie name:\t')
    #search = search.lower()
    #print(search)
#
    #search = Search(search, 'movie')
    #print(search)
    #search.search()
    #print(search.options)

    search = input('Enter actor name:\t')
    search = search.lower()
    print(search)

    search = Search(search, 'actor')
    print(search)
    search.search()
    print(search.options)



if __name__ == '__main__':
    main()

