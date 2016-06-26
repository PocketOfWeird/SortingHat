#!/usr/bin/python

# sorting-hat.py
# python 2.7.9
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
import serial
import sys
import collections

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

BASE_AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

WAIT_TIME = .5


def read_single_keypress():
    """Waits for a single keypress on stdin.
    mheyman, July 6 2011
    stackoverflow.com/question/983354/
    
    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns the character of the key that was pressed (zero on
    KeyboardInterrupt which can happen when a signal gets handled)

    """
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR 
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    try:
        ret = sys.stdin.read(1) # returns a single character
    except KeyboardInterrupt: 
        ret = 0
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return ret

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

def play_script(house):
    """
    Compiles and plays a random music and soundtrack leading to the selected house
    
    Started with Matt's code, then diverged a bit
    MIT License
    Copyright (c) 2014 Matt Backmann
    github.com/Bachmann1234/sortinghat
    """
    
    # Consider some stalling lines
    script = list_all_sound_files('stalling')
    random.shuffle(script)
    script = [get_full_path('stalling', f)
              for f in script
              if random.random() < .3]

    # Consider shouting I know!
    if random.random() < .7:
        script.append(get_random_wav_file('know'))

    # Append the house
    script.append(get_full_path('houses', house + '.wav'))

    # Play music
    music_dir = ''
    if len(script) == 2:
        music_dir = 'music_short'
    else:
        music_dir = 'music_long'
    if len(script) == 1:
        pass
    else:
        os.system('aplay ' + get_random_wav_file(music_dir) + ' &')
    time.sleep(WAIT_TIME)
    
    # Play script
    for sound in script:
        os.system('aplay ' + sound)
        time.sleep(WAIT_TIME)

def main():
    print "Sorting Hat v1.5"
    print "Press 'q' to quit"
    print "Waiting for remote input..."
    key = ""
    while key != "q":
        key = read_single_keypress()
        if HOUSE_KEYS.has_key(key):
            play_script(HOUSE_KEYS[key])
        elif OTHER_KEYS.has_key(key):
            os.system('aplay ' + get_full_path('single', OTHER_KEYS[key]))
        else:
            continue
            
main()
