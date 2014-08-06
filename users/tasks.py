from celery import Celery
from celery import shared_task

app = Celery('tasks', backend='amqp', broker='amqp://')

@shared_task
def print_hello(ignore_result=True):
    print 'hello there'

@shared_task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results