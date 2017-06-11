#!/usr/bin/python
# sorting-hat.py
#w python 2.7.9
# Author: Nathan Hartzler
# Borrowed Lots of Code from: Matt Bachman and mheyman
# License: MIT
#
# Sorting Hat python code to respond to keyboard input,
#   playback House audio files and control Animatronic servos
#

import os
import random
import time
import sys
import Adafruit_PCA9685

HOUSE_KEYS = {
    '1':'gryffindor',
    '2':'hufflepuff',
    '3':'ravenclaw',
    '4':'slytherin'
}
OTHER_KEYS = {
    '5':'weasley.wav',
    '6':'yes.wav',
    '7':'nodoubt.wav',
    '8':'no.wav',
    '9':'areyousure.wav',
    '0':'ifyouresure.wav',
    'q':'particularlydifficult.wav',
    'w':'youwouldvedonewell.wav',
    'e':'butistandbywhatisaid.wav',
    'r':'beeinbonnet.wav',
    't':'theme.wav'
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_AUDIO_DIR = os.path.join(BASE_DIR, "audio")

WAIT_TIME = .5

USE_MOUTH = True

##########################################################
#     Puppet Bits
##########################################################
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(80)


servo_start = 0
close_pos = 300
open_pos = 800

def open_mouth(num_times, sleep_time):
    for i in range(0, num_times):
	pwm.set_pwm(0, servo_start, close_pos)
	time.sleep(sleep_time)
        pwm.set_pwm(0, servo_start, open_pos)
        time.sleep(sleep_time)
        pwm.set_pwm(0, servo_start, close_pos)
        
def done_talking():
    time.sleep(.125)
    pwm.set_pwm(0,0,0)

def puppeteer(file):
    f = open(file)
    line = f.read()
    performance = line.split(',')
    sleep=0.1
    for i in range(0, len(performance)):
        direction = performance[i][0]
        number = performance[i][1:]
	if direction == 's':
            sleep=float(number)
            continue 
        if direction == 'o':
            open_mouth(int(number),sleep)
        elif direction == 'p':
            time.sleep(float(number))

##########################################################
#     File Bits
##########################################################

def list_all_sound_files(subdir):
    """
    Get all the sound files from a subdir in the audio
    folder

    MIT License
    Copyright (c) 2014 Matt Backmann
    github.com/Bachmann1234/sortinghat

    :param subdir:
        Subdir to list
    :return:
        all sound files in subdir
    """
    return [f for f in os.listdir(
        os.path.join(BASE_AUDIO_DIR, subdir)
    ) if f[-4:] == '.wav']

def get_full_path(subdir, audio_filename):
    """
    given an audio file and the subdir give a full path
    from the base sound dir

    MIT License
    Copyright (c) 2014 Matt Backmann
    github.com/Bachmann1234/sortinghat

    :param audio_filename:
        string, filename
    :return:
        full path from audio dir
    """
    return os.path.join(
        BASE_AUDIO_DIR,
        subdir,
        audio_filename
    )

def get_random_wav_file(subdir):
    """
    Used to play a sound matching a category

    MIT License
    Copyright (c) 2014 Matt Backmann
    github.com/Bachmann1234/sortinghat

    :param subdir:
        Which subdir to pull the file out of. Base dir is audio
    :return:
        A full path to the sound file chosen.
    """
    return get_full_path(
        subdir,
        random.choice(
            list_all_sound_files(subdir)
        )
    )
##########################################################
#     Play Bits
##########################################################
def play_sound(sound):
    os.system('aplay ' + sound + ' &')
    if USE_MOUTH:
        time.sleep(.25)
        puppeteer(sound + '.txt')
        done_talking()

def play_script(house):
    """
    Compiles and plays a random music and soundtrack leading to the selected house

    Started with Matt's code, then diverged a bit
    MIT License
    Copyright (c) 2014 Matt Backmann
    github.com/Bachmann1234/sortinghat
    """

    script = []
    """
    # Consider some stalling lines
    script = list_all_sound_files('stalling')
    random.shuffle(script)
    script = [get_full_path('stalling', f)
              for f in script
              if random.random() < .1]
    """
    # Consider shouting I know!
    if random.random() < .8:
        script.append(get_random_wav_file('know'))

    # Append the house
    script.append(get_full_path('houses', house + '.wav'))
    
    script_len = len(script)
   
    # Play music
    music_dir = ''
    if script_len <= 2:
        music_dir = 'music_short'
    else:
        music_dir = 'music_long'
    if script_len == 1:
        pass
    else:
        os.system('aplay ' + get_random_wav_file(music_dir) + ' &')
    time.sleep(WAIT_TIME)

    # Finally play the script
    for sound in script:
        play_sound(sound)
        time.sleep(4)

def main():
    print "Sorting Hat v1.8"
    print "Press 'z' to quit"
    key = ""
    while key != "z":
        key = str(raw_input("Waiting for remote input... "))
        print key
        if key:
            key = key[0]
            print key
        if HOUSE_KEYS.has_key(key):
            play_script(HOUSE_KEYS[key])
        elif OTHER_KEYS.has_key(key):
            single_sound = get_full_path('single', OTHER_KEYS[key])
            play_sound(single_sound)

main()
