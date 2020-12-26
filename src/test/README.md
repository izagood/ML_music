# test 설명
[music21 공식 문서](http://web.mit.edu/music21/doc/index.html)  
[music21 공식 문서 - Module Reference](http://web.mit.edu/music21/doc/moduleReference/index.html)
### 주석은 각 모듈별 .py에 있음

# testModel.py
- 매번 다른 결과를 위해 랜덤 함수를 이용하여 매번 다른 시퀀스를 입력값으로 준다.

## model.load_weights('weights.hdf5')
weights.hdf5 : trainModel.py에서 학습싴니 가중치

## generate_notes()
- 네트워크 출력 디코딩&매핑 기능 (숫자 -> categorical data)  
- 500 notes 대략 2분 노래
- 500 notes - 네트워크에 멜로디를 만들 수 있는 충분한 크기?
- 생성하려는 각 노트에 대해 네트워크에 시퀀스를 입력해야 한다.

## create_midi()
note  
chord = note + ... + note  

각 반복이 끝날때 마다 offset 0.5씩 증가(간격 동일하게 설정함)  

(note + chord) list => music streamObj