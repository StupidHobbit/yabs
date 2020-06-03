import os
import sys
import subprocess
from os import path
from time import sleep

REDIS_VERSION = '6.0.3'


def run():
    redis = run_redis()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        redis.terminate()


def run_redis():
    if not path.exists(f'redis/redis-{REDIS_VERSION}'):
        download_redis()
    os.chdir('redis')
    redis = subprocess.Popen([
        f'redis-{REDIS_VERSION}/src/redis-server',
        f'redis-{REDIS_VERSION}/redis.conf',
        '--loadmodule', 'RediSearch/src/redisearch.so'
    ], stdout=sys.stdout)
    os.chdir('..')
    return redis


def download_redis():
    if not path.exists('redis'):
        os.mkdir('redis')
    os.chdir('redis')

    subprocess.call(['wget', f'http://download.redis.io/releases/redis-{REDIS_VERSION}.tar.gz'], stdout=sys.stdout)
    subprocess.call(['tar', 'xzf', f'redis-{REDIS_VERSION}.tar.gz'], stdout=sys.stdout)
    os.chdir(f'redis-{REDIS_VERSION}')
    subprocess.call(['make'], stdout=sys.stdout)
    with open('redis.conf', 'a') as conf:
        print('unixsocket /tmp/redis.sock', file=conf)
    os.chdir('..')

    subprocess.call(['git', 'clone', '--recursive', 'https://github.com/RediSearch/RediSearch.git'], stdout=sys.stdout)
    os.chdir('RediSearch')
    subprocess.call(['make'], stdout=sys.stdout)

    os.chdir('..')


if __name__ == '__main__':
    run()
