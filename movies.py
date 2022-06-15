import requests
from numpy import nan
import re
from bs4 import BeautifulSoup

surl = 'https://www.imdb.com/find?q={}&ref_=nv_sr_sm'

cs = '<b>.*</b>\s.*\s'


class MovieThing():
    def __init__(self, code = None, html = None, session = None):
        if code is not None:
            self._from_code(code, session)
        elif html is not None:
            self._from_html(html)
        else:
            raise TypeError
        self.name = self._get_name()

    def _from_code(self, code, session):
        self.code = code
        self.url = f'https://www.imdb.com/{self.type}/{code}/?ref_=fn_al_nm_1'
        header = {'Accept-Language': 'en-US'}
        if session is None:
            self.resp = requests.get(self.url, headers = header)
        else:
            self.resp = session.get(self.url, headers = header)
        self.soup = BeautifulSoup(self.resp.content, 'html.parser')

    def _from_html(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self._get_code()
        self.url = f'https://www.imdb.com/{self.type}/{self.code}/?ref_=fn_al_nm_1'

    def _get_code(self):
        pass

    def _get_name():
        pass

    def __repr__(self):
        return '{} ({})'.format(self.name, self.code)

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)


class Actor(MovieThing):
    def __init__(self, code=None, html=None, session=None):
        self.type = 'name'
        super().__init__(code = code,
                         html = html,
                         session = session)
    
    def _get_code(self):
        code_html = self.soup.find('meta', property = 'pageId')
        self.code = code_html.attrs['content']

    def _get_name(self):
        resp = self.soup.find(class_ = 'itemprop')
        return resp.text

    def extract_movies(self):
        """
        Extract the movies of the actor.
        """
        resp = self.soup.find(class_ = 'filmo-category-section')
        jobs = resp.find_all(class_ = 'filmo-row')
        movies = []
        for job in jobs:
            head = re.search(cs, str(job))
            if re.search('<br/>', head.group()):
                job = job.find('b')
                movies.append(job)
                #print(job, '\n')
        jobs = movies

        self.job_names = [job.text for job in jobs]
        #print(self.job_names)
        self.job_urls = [job.find('a')['href'].split('/')[-2] for job in jobs]
        self.jobs = dict(zip(self.job_urls, self.job_names))
        return self.jobs


class Movie(MovieThing):
    def __init__(self, code=None, html=None, session=None):
        self.type = 'title'
        super().__init__(code = code,
                         html = html,
                         session = session)

    def _get_code(self):
        code_html = self.soup.find('meta', property = 'og:url')
        code_str = code_html.attrs['content']
        self.code = code_str.split('/')[-2]

    def _get_name(self):
        resp = self.soup.find('h1')
        return resp.text

    def _get_year(self):
        resp = self.soup.find(class_ = 'ipc-link')
        return resp.text

    def get_score(self):
        resp = self.soup.find(class_ = 'sc-7ab21ed2-1 jGRxWM')
        try:
            self.score = float(resp.text)
        except:
            self.score = nan

    def _get_cast_link(self):
        """
        The full cast is on another page. It needs to be found and followed to
        get the information.
        """
        clabel = ('ipc-metadata-list-item__label'
                  ' ipc-metadata-list-item__label--link')
        link = self.soup.find(class_ = clabel)
        return link['href']

    def get_cast(self):
        cast = Cast(self._get_cast_link())
        cast.get_cast()
        self.cast_urls = cast.cast_urls
        self.cast_names = cast.cast_names
        self.cast = dict(zip(self.cast_urls, self.cast_names))
        return self.cast

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __eq__(self, other):
        return self.score == other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __gt__(self, other):
        return self.score >= other.score


class Cast():
    def __init__(self, code):
        self.url = 'http://www.imdb.com{}'.format(code)
        headers = {'Accept-Language': 'en-US'}
        self.resp = requests.get(self.url, headers = headers)
        self.soup = BeautifulSoup(self.resp.content, 'html.parser')

    def get_cast(self):
        """
        Get list of cast members and URL 'constructors'.
        """
        h = self.soup.find(class_ = 'cast_list')
        cast_list = h.find_all(class_ = 'primary_photo')
        self.cast_urls = [actor.find('a')['href'].split('/')[-2]
                          for actor in cast_list]
        self.cast_names = [actor.find('img')['title'] for actor in cast_list]
        self.cast = dict(zip(self.cast_urls, self.cast_names))


def search_imdb(query):
    """
    Search a query on imbd.
    """
    query = query.split()
    query = '+'.join(query)
    resp = requests.get(surl.format(query))
    print(resp.headers)



if __name__ == '__main__':
    a = Actor('nm0001548')
    print(a.resp)
    print(a.job_names)
    print(a.job_urls)
    
    print('')

    m = Movie('tt0098067')
    print(m.resp)
    m._get_cast_link()
    print(m.cast_names)
    print(m.cast_urls)
