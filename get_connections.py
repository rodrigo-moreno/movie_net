from movies import *
from requests import Session
import cProfile
import pstats
import sys
import httpx
import asyncio


async def get_connections(movie):
    movie = Movie(movie)
    movie.get_cast()
    print(movie.name)

    c = set()

    url = 'https://www.imdb.com/name/{}/?req_=fn_al_1'
    header = {'Accept-Language': 'en-US'}

    async with httpx.AsyncClient() as client:
        #tasks = (Actor(code) for code in movie.cast_urls)
        tasks = (client.get(url.format(code), headers = header) for code in movie.cast_urls)
        reqs = await asyncio.gather(*tasks)

    actors = [Actor(html = resp.content) for resp in reqs]
    for actor in actors:
        print(actor.name)
        actor.extract_movies()
        for k, v in actor.jobs.items():
            c.add((k, v))

    print(c)


def main():
    movie = sys.argv[1]
    
    with cProfile.Profile() as pr:
        asyncio.run(get_connections(movie))

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename = 'conn.prof')


if __name__ == '__main__':
    main()

