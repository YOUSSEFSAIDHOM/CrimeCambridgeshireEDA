
###
""" 
This script fetches data from https://data.police.uk
For this coursework, Cambridgeshire will be the local area considered
"""
###


urls = ['https://data.police.uk/data/archive/2019-01.zip',
        'https://data.police.uk/data/archive/2019-02.zip',
        'https://data.police.uk/data/archive/2019-03.zip',
        'https://data.police.uk/data/archive/2019-04.zip',
        'https://data.police.uk/data/archive/2019-05.zip',
        'https://data.police.uk/data/archive/2019-06.zip',
        'https://data.police.uk/data/archive/2019-07.zip',
        'https://data.police.uk/data/archive/2019-08.zip',
        'https://data.police.uk/data/archive/2019-09.zip',
        'https://data.police.uk/data/archive/2019-10.zip',
        'https://data.police.uk/data/archive/2019-11.zip',
        'https://data.police.uk/data/archive/2019-12.zip',
        'https://data.police.uk/data/archive/2020-01.zip',
        'https://data.police.uk/data/archive/2020-02.zip',
        'https://data.police.uk/data/archive/2020-03.zip',
        'https://data.police.uk/data/archive/2020-04.zip',
        'https://data.police.uk/data/archive/2020-05.zip',
        'https://data.police.uk/data/archive/2020-06.zip',
        'https://data.police.uk/data/archive/2020-07.zip',
        'https://data.police.uk/data/archive/2020-08.zip',
        'https://data.police.uk/data/archive/2020-09.zip',
        'https://data.police.uk/data/archive/2020-10.zip',
        'https://data.police.uk/data/archive/2020-11.zip',
        'https://data.police.uk/data/archive/2020-12.zip',
        'https://data.police.uk/data/archive/2021-01.zip',
        'https://data.police.uk/data/archive/2021-02.zip',
        'https://data.police.uk/data/archive/2021-03.zip',
        'https://data.police.uk/data/archive/2021-04.zip',
        'https://data.police.uk/data/archive/2021-05.zip',
        'https://data.police.uk/data/archive/2021-06.zip',
        'https://data.police.uk/data/archive/2021-07.zip',
        'https://data.police.uk/data/archive/2021-08.zip',
        'https://data.police.uk/data/archive/2021-09.zip',
        'https://data.police.uk/data/archive/2021-10.zip',
        'https://data.police.uk/data/archive/2021-11.zip',
        'https://data.police.uk/data/archive/2021-12.zip']

# files = ['2019-01/2019-01-cambridgeshire-outcomes.csv',
#          '2019-02/2019-02-cambridgeshire-outcomes.csv',
#          '2019-03/2019-03-cambridgeshire-outcomes.csv',
#          '2019-04/2019-04-cambridgeshire-outcomes.csv',
#          '2019-05/2019-05-cambridgeshire-outcomes.csv',
#          '2019-06/2019-06-cambridgeshire-outcomes.csv',
#          '2019-07/2019-07-cambridgeshire-outcomes.csv',
#          '2019-08/2019-08-cambridgeshire-outcomes.csv',
#          '2019-09/2019-09-cambridgeshire-outcomes.csv',
#          '2019-10/2019-10-cambridgeshire-outcomes.csv',
#          '2019-11/2019-11-cambridgeshire-outcomes.csv',
#          '2019-12/2019-12-cambridgeshire-outcomes.csv',
#          '2020-01/2020-01-cambridgeshire-outcomes.csv',
#          '2020-02/2020-02-cambridgeshire-outcomes.csv',
#          '2020-03/2020-03-cambridgeshire-outcomes.csv',
#          '2020-04/2020-04-cambridgeshire-outcomes.csv',
#          '2020-05/2020-05-cambridgeshire-outcomes.csv',
#          '2020-06/2020-06-cambridgeshire-outcomes.csv',
#          '2020-07/2020-07-cambridgeshire-outcomes.csv',
#          '2020-08/2020-08-cambridgeshire-outcomes.csv',
#          '2020-09/2020-09-cambridgeshire-outcomes.csv',
#          '2020-10/2020-10-cambridgeshire-outcomes.csv',
#          '2020-11/2020-11-cambridgeshire-outcomes.csv',
#          '2020-12/2020-12-cambridgeshire-outcomes.csv',
#          '2021-01/2021-01-cambridgeshire-outcomes.csv',
#          '2021-02/2021-02-cambridgeshire-outcomes.csv',
#          '2021-03/2021-03-cambridgeshire-outcomes.csv',
#          '2021-04/2021-04-cambridgeshire-outcomes.csv',
#          '2021-05/2021-05-cambridgeshire-outcomes.csv',
#          '2021-06/2021-06-cambridgeshire-outcomes.csv',
#          '2021-07/2021-07-cambridgeshire-outcomes.csv',
#          '2021-08/2021-08-cambridgeshire-outcomes.csv',
#          '2021-09/2021-09-cambridgeshire-outcomes.csv',
#          '2021-10/2021-10-cambridgeshire-outcomes.csv',
#          '2021-11/2021-11-cambridgeshire-outcomes.csv',
#          '2021-12/2021-12-cambridgeshire-outcomes.csv']

files = [
         '2018-01/2018-01-cambridgeshire-outcomes.csv',
         '2018-02/2018-02-cambridgeshire-outcomes.csv',
         '2018-03/2018-03-cambridgeshire-outcomes.csv',
         '2018-04/2018-04-cambridgeshire-outcomes.csv',
         '2018-05/2018-05-cambridgeshire-outcomes.csv',
         '2018-06/2018-06-cambridgeshire-outcomes.csv',
         '2018-07/2018-07-cambridgeshire-outcomes.csv',
         '2018-08/2018-08-cambridgeshire-outcomes.csv',
         '2018-09/2018-09-cambridgeshire-outcomes.csv',
         '2018-10/2018-10-cambridgeshire-outcomes.csv',
         '2018-11/2018-11-cambridgeshire-outcomes.csv',
         '2018-12/2018-12-cambridgeshire-outcomes.csv',]

from remotezip import RemoteZip

# for f, b, in zip(urls, files):
#     with RemoteZip(f) as zip:
#         zip.extract(b)

from importlib import reload
import Functions
reload(Functions)

import requests
import zipfile
import io
import os
from datetime import datetime
import pandas as pd

from Functions import *

base_dir = 'prepan_data'

output = 'National_Crime_Recs_PM_(BY_TYPE_PREPAN).csv'

crime_summary = summarise_crime_types_per_month(base_dir)

crime_summary.to_csv(output, index=False)
print("done")
