import json
from pyignite import Client
from pyignite.datatypes.cache_config import CacheMode
from pyignite.datatypes.prop_codes import *
from pyignite.exceptions import SocketError
import argparse

storage={
    'id':"storage-id-1234",
    'accessCount': 0,
}
usecase={
    'id':"usecase-id-1234",
    'accessCount': 0,
}

def buildkey(a):
    return "/".join([a.split('-')[0], a])

def prime_cache(usecase, storage):
    cache.put(buildkey(storage['id']), json.dumps(storage))
    cache.put(buildkey(usecase['id']), json.dumps(usecase))

def access_cache(usecase, storage): 
    values = cache.get_all([buildkey(usecase['id']), buildkey(storage['id'])])
    storage = json.loads(values[buildkey(storage['id'])])
    usecase = json.loads(values[buildkey(usecase['id'])])
    storage['accessCount']+=1
    usecase['accessCount']+=1
    cache.put(buildkey(storage['id']), json.dumps(storage))
    cache.put(buildkey(usecase['id']), json.dumps(usecase))

    print(storage['accessCount'])
    print(usecase['accessCount'])

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--prime', dest='prime', action='store_true')
args = parser.parse_args()


nodes = [
    ('172.17.0.21', 10800),
    ('172.17.0.22', 10800),
]


client = Client(timeout=4.0)
client.connect(nodes)
print('Connected to {}'.format(client))

cache = client.get_or_create_cache({
    PROP_NAME: 'cache',
    PROP_CACHE_MODE: CacheMode.PARTITIONED,
    PROP_BACKUPS_NUMBER: 1
})

triesLeft=2
while triesLeft > 0:
    try:
        if args.prime: 
            prime_cache(usecase, storage)
        access_cache(usecase, storage)
        print("Success")
        triesLeft=0
    except (OSError, SocketError) as e:
        print('Error: {}'.format(e))
        triesLeft-=1


