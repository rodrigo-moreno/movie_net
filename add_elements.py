import requests
from bs4 import BeautifulSoup
import csv
import re
from numpy import nan
from cast_intersection import cast_intersection


class Option():
    '''
    An object to represent a single option from IMDB search.
    '''
    def __init__(self, soup, pos, type_):
        self.soup = soup
        self.type = type_
        self.pos = pos + 1
        self._get_code()
        self._get_name()
        if self.type == 'movie':
            self._get_year()

    def __repr__(self):
        if self.type == 'movie':
            out = f'[{self.pos}] {self.name} ({self.year}): {self.code}'
        elif self.type == 'actor':
            out = f'[{self.pos}] {self.name}: {self.code}'
        return out

    def __str__(self):
        if self.type == 'movie':
            out = f'[{self.pos}] {self.name} ({self.year}): {self.code}'
        elif self.type == 'actor':
            out = f'[{self.pos}] {self.name}: {self.code}'
        return out

    def _get_code(self):
        href = self.soup.find('a')
        href = href.attrs['href']
        self.code = href.split('/')[2]

    def _get_name(self):
        if self.type == 'movie':
            self.name = self.soup.find_all('a')[1].text
        elif self.type == 'actor':
            self.name = self.soup.find_all('a')[1].text

    def _get_year(self):
        text = self.soup.text.strip()
        try:
            re_match = re.search('\((\d*)\)', text)
            self.year = re_match.group(1)
        except:
            self.year = nan
        pass


class Options():
    '''
    An object...
    '''
    def __init__(self, options, type_):
        self.options = [Option(soup, pos, type_) for (pos, soup) in enumerate(options)]
        self.positions = [ii + 1 for ii in range(len(self.options))]

    def __repr__(self):
        out = f'List of {len(self.options)} options\n'
        for option in self.options:
            out += f'{option}\n\n'
            #out += f'[{pos + 1}] {option}\n\n'
        return out

    def __str__(self):
        out = f'List of {len(self.options)} options\n'
        for option in self.options:
            out += f'{option}\n\n'
            #out += f'[{pos + 1}] {option}\n\n'
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
        #indexes = 
        opts = self.options[start: start + n]
        out = [opt.__repr__() for opt in opts]
        out = '\n'.join(out)
        return out + '\n'
        #print('\n'.join(out))


class Search():
    '''
    An object to represent a search result from IMDB.
    '''
    def __init__(self, keywords, type_):
        self.keywords = keywords.lower()
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
            text = self.options.display(start = rounds * 5, n = 5)
            #self.options.display(start = rounds * 5, n = 5)
            selection = input(text)
            if selection.isnumeric():
                selection = int(selection)
                found = True
                return self.options.options[selection - 1]
            else:
                rounds += 1





#################################################################################
################################################################################
################################################################################
### FUNCTIONS
def inquire(s_type):
    '''
    A function...
    '''
    search = input(f'Enter {s_type} name:\t')
    search = Search(search, s_type)
    search.search()
    choice = search.choose()
    return choice

def choose_from_list(opt_list):
    '''
    A function...
    '''
    found = False
    rounds = 0
    while not found:
        opts = opt_list[rounds * 5 : rounds * 5 + 5]
        opts = [actor.__repr__() for actor in opts]
        text = '\n'.join(opts)
        query = input(text + '\n')
        if query.isnumeric():
            selection = int(query)
            found = True
            return opt_list[selection - 1]
        else:
            rounds += 1





###############################################################################
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

    movie = inquire('movie')
    #print(movie)

    while True:
        prompt = ('Do you know the name of the connecting actor?\n'
                  'If so, press [1]. Else, press [2].\n'
                 )
        choice = input(prompt)
        if choice == '1':
            actor = inquire('actor')
            #print(actor)
            break
        elif choice == '2':
            #print('You chose the intersection method.')
            intersection = cast_intersection(movie.code, movies[-1])
            #print(intersection)
            actor = choose_from_list(intersection)
            #print(actor)
            break
        else:
            print('Please enter a valid answer.')
    
    print(f'The choices are:\n\t{movie.name}\n\t{actor.name}')
    print((f'The output text will be:\n'
           f'{movie.code}, {actor.code}'
           )
          )
    with open('history.csv', 'a') as f:
        f.write(f'\n{movie.code}, {actor.code}')



if __name__ == '__main__':
    main()

