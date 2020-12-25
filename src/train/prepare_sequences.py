"""
prepare_sequences.py
--------------------
mid파일에서 받은 notes와 notes들의 집합 n_vocab을 매개변수로 받아
(network_input, network_output)를 return 한다.

"""
import glob
import pickle
import numpy

from music21 import instrument
from music21 import converter
from music21 import note
from music21 import chord

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.utils import np_utils
from tensorflow.keras.callbacks import ModelCheckpoint

# get_notes주석은 get_notes.py에 있음


def get_notes():
    notes = []

    for file in glob.glob("../../midi_songs/*.mid"):

        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try:
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse()
        except Exception:
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes


# 매개변수 기본 세팅
notes = get_notes()  # list
n_vocab = len(set(notes))  # int


def prepare_sequences(notes, n_vocab):
    """
    뉴런 네트워크를 이용해서 시퀀스를 준비한다.
    """
    # 시퀀스 길이 100
    sequence_length = 100

    # get all pitch names
    # 모든 계이름을 가져온다.
    pitchnames = sorted(set(item for item in notes))

    # create a dictionary to map pitches to integers
    # 정수에 계이름을 매핑하는 dictionary을 만든다.
    # enumerate로 pitch가 정수로 열거되면 해당 정수를 note에 매핑해준다.
    note_to_int = dict((note, number)
                       for (number, note) in enumerate(pitchnames))

    # 네트워크 입력과 출력
    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    # 입력 시퀀스 및 해당 출력을 생성한다.
    for i in range(0, len(notes) - sequence_length, 1):

        # sequence in, out
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]

        # network input, out
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    # LSTM 레이어와 호환되는 형식으로 입력 내용을 변경한다.
    network_input = numpy.reshape(
        network_input,
        (n_patterns, sequence_length, 1)
    )

    # normalize input
    # input 정상화
    network_input = network_input / float(n_vocab)

    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)


if __name__ == '__main__':
    prepare_sequences(notes, n_vocab)
