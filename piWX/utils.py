import os
import time

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def textType(text, delay=0.035):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print('\r')
