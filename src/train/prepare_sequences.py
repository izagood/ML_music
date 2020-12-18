""" This module prepares midi file data and feeds it to the neural network for training """

import glob
import pickle
import numpy

import music21.converter as converter
import music21.instrument as instrument
import music21.note as note
import music21.chord as chord

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.utils import np_utils
from tensorflow.keras.callbacks import ModelCheckpoint

def get_notes():
    """ 모든 note 와 chors 는 ./midi_songs 경로에 있는 mid files에 있다."""
    # notes 리스트
    notes = []

    for file in glob.glob("../../midi_songs/*.mid"):

        """ file을 music21을 streamObj로 로드(load)
            streamObj를 사용하면 파일에 있는 모든 note와 chord 목록이 나온다.
            note - 계이름(pitch)의 문자열 표기법을 사용하여 다시 만들 수 있으므로
            모든 note 객체의 계이름을 문자열 표기법으로 추가한다.
            그리고 각 note를 점(.)로 나누어 현 안에 있는 모든 음들의 id를 하나의 문자열로 인코딩해서
            모든 화음을 추가한다.
            이러한 인코딩을 통해 생성된 출력을 올바른 note와 chrod로 쉽게 디코딩할 수 있다."""
        midi = converter.parse(file)
        
        print("Parsing %s" % file)

        notes_to_parse = None

        try:
            # file에 instrument parts가 있을 때
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse()
        except Exception:
            # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes

notes = get_notes()
n_vocab = len(set(notes))

def prepare_sequences(notes, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 100

    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

    # create a dictionary to map pitches to integers
    note_to_int = dict((note, number)
                       for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = numpy.reshape(
        network_input, (n_patterns, sequence_length, 1))
    # normalize input
    network_input = network_input / float(n_vocab)

    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)

if __name__ == '__main__':
    prepare_sequences(notes, n_vocab)
