#!/usr/bin/env python3

import configparser
from subprocess import getoutput

config = configparser.RawConfigParser()
config.read(cfg_file)

url = config['PRED']['URL']
filename = config['COMMON']['DATA_PATH'] + "/res.txt"

# duration of alarm
duration_alarm = 33
duration_alarm = int(config['PRED']['duration_alarm'])

prediction_buffer = 5
prediction_buffer = int(config['PRED']['prediction_buffer'])

threshold = 50
threshold = int(config['PRED']['threshold'])

status = getoutput('tail -1 ' + filename)
status0 = '{"tag":[],"filename":"jpg","receivetime":"1999/13/32 25:00:67"}'

now = datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S')

