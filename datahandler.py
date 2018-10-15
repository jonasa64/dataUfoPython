import os
import urllib.request as req
import pandas as pd
from states import states_us, states_ca

DEFAULT_URL = 'https://raw.githubusercontent.com/planetsig/ufo-reports/master/csv-data/ufo-scrubbed-geocoded-time-standardized.csv'
DEFAULT_PATH = 'ufo.csv'
DEFAULT_HEADERS = ['Datetime',
                   'City',
                   'State',
                   'Country',
                   'Shape',
                   'Duration',
                   'DurationLiteral',
                   'Comments',
                   'PostDate',
                   'Lat',
                   'Lon',
                  ]

# Function to download a given url
def download(url, to=None):
    '''
    Downloads a file from a given url(arg1) and return the relative file name
    :param url: Address of the file to download
    :param to: URL of the file to download to - if none is specified, download to current folder and keep it's file name
    :return: Returns the relative path for futher usage(e.g to open the file)
    '''
    print("Downloading file ...")
    opener = req.build_opener()
    # add headers imitating a browser to enforce download permission from all websites
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')]
    req.install_opener(opener)
    req.urlretrieve(url, to)
    print("Done")

    return to

def getUfoData(url = DEFAULT_URL):
    '''
    Loads the dataset from 'url' into Pandas Dataframe and returns it
    :param url: url to dataset - default is constant DEFAUL_URL
    :return: Pandas Datafram
    '''
    if not os.path.isfile(DEFAULT_PATH):
        download(url, DEFAULT_PATH)

    result = pd.read_csv(DEFAULT_PATH, dtype='unicode', low_memory=False, names=DEFAULT_HEADERS)

    return result

df = getUfoData() # Load dataframe

states = dict(states_us, **states_ca)

#Hvilket sted er der flest UFO observationer?


#Hvordan har antallet af observationer udviklet sig over tid?

#Som besvarelse til det her spørgsmål vil det give god mening at lave et plot. Det er valgfrit, hvordan i laver plottet.

#Hvornår på året er der flest observationer?

#Hvordan ser en ufo ud?

#Find flere buzzwords som f.eks. form, farve eller andet. Her kan det være en fordel at bruge textBlob. https://textblob.readthedocs.io/en/dev/

#Hvor lang tid kunne de se ufoen(gennemsnit)?
