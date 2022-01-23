import gzip
import requests

base_url = r'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/'

stations = [
    "MY000096465",
    "MY000096491",
    "MYM00048601",
    "MYM00048615",
    "MYM00048647",
    "MYM00048650",
    "MYM00048665",
    "MYM00048674",
    "MYM00096421",
    "MYM00096449",
    "MYM00096471",
    "MYM00096481",
    "MY000048620",
    "MY000048657",
    "MY000096413",
    "MY000096441",    
    ]

for stn in stations:
    url = base_url + stn + '.csv.gz'
    response = requests.get(url)
    body = response.content
    csv = gzip.decompress(body)
    f = open(stn+'.csv', 'wb')
    f.write(csv)
    f.close()
