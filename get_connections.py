"""
A script that finds the connections of a movie and sorts them according to
their ranking.
"""
from movies import *
from requests import Session
import cProfile
import pstats
import sys
import httpx
import asyncio
import csv


smovies = set()
uactors = set()

with open('history.csv', newline = '') as f:
    data = csv.reader(f)
    for row in data:
        smovies.add(row[0].strip())
        uactors.add(row[1].strip())


async def get_connections(movie):
    """
    Get a set of movie codes that connect with a given movie.

    Input:
    - movie: A movie code from which a movies.Movie() object can be created.

    Outpt:
    - c: a set() of connections.
    """
    movie = Movie(movie)
    movie.get_cast()
    print(movie.name)
    cast = set(movie.cast_urls)
    available = cast - uactors

    c = set()

    url = 'https://www.imdb.com/name/{}/?req_=fn_al_1'
    header = {'Accept-Language': 'en-US'}

    async with httpx.AsyncClient() as client:
        #tasks = (Actor(code) for code in movie.cast_urls)
        tasks = (client.get(url.format(code), headers = header) for code in available)
        reqs = await asyncio.gather(*tasks)

    actors = [Actor(html = resp.content) for resp in reqs]
    for actor in actors:
        #print(actor.name)
        actor.extract_movies()
        for k, v in actor.jobs.items():
            c.add(k)
    c = c - smovies

    return c


async def sort_connections(movie_set):
    """
    Sort a set of movie codes according to their movie scores in IMDB.

    Input:
    - movie_set: A set of movie codes.

    Output:
    - None
    """
    url = 'https://www.imdb.com/title/{}/?req_=fn_al_1'
    header = {'Accept-Language': 'en-US'}
    movie_set = list(movie_set)
    movies = []
    ii = 1

    while movie_set:
        print(f'On round {ii}.')
        cs = 10
        cms = movie_set[:cs]
        del movie_set[:cs]
        async with httpx.AsyncClient() as client:
            tasks = (client.get(url.format(code), headers = header) for code in cms)
            reqs = await asyncio.gather(*tasks)
        cmovies = [Movie(html = resp.content) for resp in reqs]
        movies.extend(cmovies)
        ii += 1
    print('Finished making movies.')

    #movies = [Movie(html = resp.content) for resp in reqs]
    for movie in movies:
        #print(movie.name)
        movie.get_score()

    movies.sort()
    print(movies)
    return movies


def main():
    movie = sys.argv[1]

    with cProfile.Profile() as pr:
        conn_set = asyncio.run(get_connections(movie))
        #conn_set = set(list(conn_set)[:10])
        asyncio.run(sort_connections(conn_set))
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename = 'conn.prof')


if __name__ == '__main__':
    main()

