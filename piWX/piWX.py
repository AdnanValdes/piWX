#!/usr/bin/env python

import os
import time
import argparse
import requests
from avwx import Metar, Taf
from utils import clear, textType

def update(airports):
    for airport in airports:
        exec(f'{airport}.update()')
        exec(f'{airport}_taf.update()')

def display(airports, speed, metar, taf, pause):
    clear()
    for airport in airports:
        if taf:
            textType(f'{airport.upper()} METAR', speed)
            exec(f"textType({airport}.raw, {speed})")
            #print('\n')
        if metar:
            textType(f'{airport.upper()} TAF', speed)
            exec(f"textType({airport}_taf.raw, {speed})")
            #print('\n')
        print('\n')
    time.sleep(pause)

def wttr(airports, speed, pause):
    wx = requests.get('http://wttr.in')
    clear()
    print(wx.text)
    time.sleep(pause*2)


parser = argparse.ArgumentParser(description='An aviation weather streaming service.')
parser.add_argument('airports', nargs='*')
parser.add_argument('--wttr', help='Show wttr.in weather dashboard after each cycle. It will be displayed twice as long as the --pause value', action='store_true')
parser.add_argument('--stream', help='Alternative mode. Displays a constant stream of observations and forecasts. A new line will be printed whenever the METAR or TAF is updated. The display will not be cleared.', action='store_true')
parser.add_argument('-s', '--speed', type=int, help='Set text typing speed. Default is 0.035.', default=0.035)
parser.add_argument('-p', '--pause', type=int, help='Set pause timer between screen changes. If you want fewer screen changes, set a higher value. Value is in seconds; default is 3. If the script is set to --stream mode, the pause argument defines how often the program will check if there is an update by sending a GET request. For --stream mode, the pause value = pause*2', default=3)
parser.add_argument('-m', '--metar', help='Use this flag to display METARs only', action='store_false')
parser.add_argument('-t', '--taf', help='Use this flag to display TAFs only', action='store_false')
args = parser.parse_args()

airports = args.airports

for airport in airports:
    exec(f'{airport} = Metar("{airport.upper()}")')
    exec(f'{airport}_taf = Taf("{airport.upper()}")')



while True:
    if args.stream:
        for airport in airports:
            if (eval(f'{airport}.update()') and args.taf) or (eval(f'{airport}_taf.update()') and args.metar):
                if args.taf:
                    try:
                        exec(f'{airport}.update()')
                        exec(f"textType({airport}.raw, {args.speed})")
                    except TypeError:
                        continue
                if args.metar:
                    try:
                        exec(f'{airport}_taf.update()')
                        exec(f"textType({airport}_taf.raw, {args.speed})")
                    except TypeError:
                        continue
                print('\n')
        time.sleep(args.pause*2)

    else:
        update(airports)
        flight_rules = [exec(f"{airport}.data.flight_rules") for airport in airports]

        display(airports, args.speed, args.metar, args.taf, args.pause)

        if args.wttr:
            wttr(airports, args.speed, args.pause)


# fix newline after METAR if no TAF
