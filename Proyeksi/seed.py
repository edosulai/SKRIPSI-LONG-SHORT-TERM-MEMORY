#!/usr/bin/env python

"""
    Script to import data from .csv file to Model Database DJango
    To execute this script run: 
                                1) manage.py shell
                                2) exec(open('file_name.py').read())
"""

from asyncio.windows_events import NULL
import csv
from datetime import datetime
from proyeksi.models import Klimatologi

CSV_PATH = '../Assets/Data/1985-2021.csv'

with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    for row in spamreader:
        Klimatologi.objects.create(
            tanggal=datetime.strptime(row[0], '%d-%m-%Y').strftime('%Y-%m-%d'),
            tn=row[1] if row[1] else NULL,
            tx=row[2] if row[2] else NULL,
            tavg=row[3] if row[3] else NULL,
            rh_avg=row[4] if row[4] else NULL,
            rr=row[5] if row[5] else NULL,
            ss=row[6] if row[6] else NULL,
            ff_x=row[7] if row[7] else NULL,
            ddd_x=row[8] if row[8] else NULL,
            ff_avg=row[9] if row[9] else NULL,
            ddd_car=row[10] if row[10] else NULL
        )

# exec(open('seed.py').read())