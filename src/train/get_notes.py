""" This module prepares midi file data and feeds it to the neural network for training """

import glob
import pickle

from music21 import instrument
from music21 import converter
from music21 import note
from music21 import chord

def get_notes():
    """ 모든 note 와 chors 는 ./midi_songs 경로에 있는 mid files에 있다."""
    # notes 리스트
    notes = []
    
    """ glob - 디렉토리에 있는 파일 읽어오기 """
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



if __name__ == '__main__':
    get_notes()
