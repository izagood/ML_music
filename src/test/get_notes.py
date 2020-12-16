""" This module prepares midi file data and feeds it to the neural network for training """

import glob
import pickle

import music21.converter as converter
import music21.instrument as instrument
import music21.note as note
import music21.chord as chord

def get_notes():
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    # notes 리스트
    notes = []

    for file in glob.glob("../../midi_songs/*.mid"):
        # file을 music21을 streamObj로 변환
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
