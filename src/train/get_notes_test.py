""" This module prepares midi file data and feeds it to the neural network for training """

import glob
import pickle
from typing import Any

from music21 import *


us = environment.UserSettings()
# for key in sorted(us.keys()):
#     print(key)
# us['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'

n = note.Note("D#3")
n.duration.type = 'half'
n.show()
# us['musescoreDirectPNGPath'] = 'C:/Program Files/MuseScore 3/bin/MuseScore3.exe'
# print(us['musescoreDirectPNGPath'])