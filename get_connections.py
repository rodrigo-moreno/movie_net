from script import *
import sys

movie = sys.argv[1]
try:
    actor = sys.argv[2]
except:
    actor = ''

#print(movie)
#print(actor)

movie = Movie(movie)
print(movie.name)

c = set()
for a in movie.cast_urls:
    if a == actor:
        print('Skipping this because it is undesired.')
    else:
        c_actor = Actor(a)
        print(c_actor.name)
        for job in c_actor.job_names:
            c.add(job)

print(c)

