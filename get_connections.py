from movies import *
from requests import Session
#import logging
import cProfile
import pstats
import sys

#requests.packages.urllib3.util.connection.HAS_IPV6 = False


#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger('requests.packages.urllib3')
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True


def main():
    movie = sys.argv[1]
    try:
        actor = sys.argv[2]
    except:
        actor = ''

    s = Session()

    #print(movie)
    #print(actor)

    movie = Movie(movie, session = s)
    movie.get_cast()
    print(movie.name)

    c = set()
    for a in movie.cast_urls:
        if a == actor:
            print('Skipping this because it is undesired.')
        else:
            c_actor = Actor(a, session = s)
            c_actor.extract_movies()
            print(c_actor.name)
            for job in c_actor.job_urls:
                job = Movie(job, session = s)
                c.add(job)

    print(c)


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    #stats.print_stats()
    stats.dump_stats(filename = 'connections_nonipv4.prof')

