"""
get_notes.py
------------
midi file을 불러와서 music21의 note와 chord형식으로 변환해주는 모듈이다.

모든 note 와 chors 는 ./midi_songs 경로에 있는 mid files에 있다.

file을 music21을 사용하여 streamObj로 로드(load)한다.
streamObj를 사용하면 파일에 있는 모든 note와 chord 목록이 나온다.

note - 계이름(pitch)의 문자열 표기법을 사용하여 다시 만들 수 있으므로
모든 note 객체의 계이름을 문자열로 추가한다.

그리고 각 note를 점(.)으로 나누어 현 안에 있는 모든 음들의 id를 하나의 
문자열로 인코딩해서 모든 화음을 추가한다.
이러한 인코딩을 통해 생성된 출력을 
올바른 note와 chrod로 쉽게 디코딩할 수 있다.
"""
import glob
import pickle

from music21 import instrument
from music21 import converter
from music21 import note
from music21 import chord


# notes 리스트
notes = []

""" 
glob - 디렉토리에 있는 파일 읽어오기
glob이 읽어 올때 list 형식으로 읽어온다.
"""
for file in glob.glob("./midi_songs/*.mid"):
    """
    @  function converter.parse() - 음악 로드
    @  param value: Union[music21.metadata.bundles.MetadataEntry, bytes, str, pathlib.Path], *args, **keywords
    @return music21.stream.Stream
    ----------------------------------------
    converter.parse()는 string 형식으로 들어와야 하기 때문에 단독 midi file을
    불러올 때는 file[n] 형식으로 불러와서 사용해야 함. 
    """
    midi = converter.parse(file)

    print("Parsing %s" % file)

    # note 를 분할?
    notes_to_parse = None

    # file에 instrument parts가 있을 때
    try:
        """
        @function instrument.partitionByInstrument()
        @param streamObj
        @return Score
        -------------------------------------------
        단일 streamObj 또는 score 또는 유사한 다중 부분 구조(여러 악기가 합쳐진 구조)가 주어지면
        각 고유 악기에 대해 부분으로 나누고 각 악기별로 합친다.
        """
        s2 = instrument.partitionByInstrument(midi)

        """
        함수 체인
        Score -> stream.Part() -> stream.recurse()
        ------------------------------------------
        @class music21.stream.Part(*args, **keywords)
        ----------------------------------------------
        A Stream subclass for designating music that is considered a single part.
        단일 part로 간주되는 음악을 지정하기 위한 단일 stream 하위 클래스이다.

        When put into a Score object,
        Score 객체에 넣었을 때
        
        Part objects are all collected in the Score.parts call. 
        Score.parts 호출에 모두 Part 객체가 수집된다.

        Otherwise they mostly work like generic Streams.
        그렇지 않으면 대부분 일반적인 Streams처럼 작동한다

        Generally the hierarchy goes: Score > Part > Measure > Voice, 
        일반적으로 Score > Part > Measure > Voice 순으로 지정되지만,
        
        but you are not required to stick to this.
        이렇게 사용해야하는건 아님.

        Part groupings (piano braces, etc.) are found in the music21.layout module in the StaffGroup Spanner object.
        Part grouping(피아노 braces 등)은 Staff Group Spanner 객체의 music21.layout 모듈에 있다.
        --------------------------------------------------------------------------------------
        Stream.recurse(*, streamsOnly=False, restoreActiveSites=True, 
        classFilter=(), skipSelf=True, includeSelf=None)
        -------------------------------------------------
        반복(iterate)할 수 있는 iterator로 리턴해줌.
        """
        notes_to_parse = s2.parts[0].recurse()

    # file has notes in a flat structure 일때
    except Exception:
        """
        music21.stream.Stream.flat.notes
        """
        notes_to_parse = midi.flat.notes

    # parse 된 노트들의 엘리먼트 for문
    for element in notes_to_parse:
        # note.Note
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        # chord.Chord
        elif isinstance(element, chord.Chord):
            # normal Order를 하나씩 빼서 .으로 join해서 notes에 붙여
            notes.append('.'.join(str(n) for n in element.normalOrder))

with open('data/notes2', 'wb') as filepath:
    # notes를 해당 경로에 pickle.dump로 전부 쓰기
    pickle.dump(notes, filepath)

print(notes)
