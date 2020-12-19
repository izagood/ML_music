""" This module prepares midi file data and feeds it to the neural network for training """

import glob
import pickle
from typing import Any

from music21 import instrument
from music21 import converter
from music21 import note
from music21 import chord


""" 모든 note 와 chors 는 ./midi_songs 경로에 있는 mid files에 있다."""

# glob - 디렉토리에 있는 파일 읽어오기
for file in glob.glob("./midi_songs/*.mid"):
    
    midi = converter.parse(file)
    
    print("Parsing %s" % file)
    
    print(midi)
