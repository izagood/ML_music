""" This module prepares midi file data and feeds it to the neural network for training """

import glob
import pickle
from typing import Any

from music21 import *


us = environment.UserSettings()
us.create()
us['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'

n = note.Note("D#3")
n.duration.type = 'half'
n.show()
