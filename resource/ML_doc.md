# ML 정리

## ML
- 숫자 기반 데이터를 신경망이 더 잘 학습함

## RNN
- 순차 정보

## LSTM
- gradient descent(기울기 하상)
- 네트워크가 장기 기억해야할 때 유용한 방법
- music, text 생성에 잘 맞는 기법

# music21
### music21.converter
다양한 음악 파일 포맷으로부터 음악을 로드하는 툴  

### music21.converter.parse()
파일의 item을 파싱하고 stream에 넣어줌  
@param string  

---------------------------------------------
### music21.instrument.partitionByInstrument()
단일 stream, score, multi part 구조인 경우에 각각의  
악기별로 파티션을 나누고 다른 part들을 악기별로 합쳐준다.  

### music21.stream.recurse()
stream 안에 존재하는 music21 객체가 가지고 있는 값들의 list를  
반복(iterate)할 수 있는 iterator로 return해준다.

# Tensorflow

## Model
### Model 사용
- 첫번째 layer에서는 input_shape라는 고유의 매개변수 필요
=> 네트워크에 데이터의 형태를 알려줌
- 마지막 layer는 다른 함수들과 node 수를 일치시켜야 한다.  
-------------------------------------------------------

#### LSTM layer
@param_1 layer의 노드 수  

-------------------------
어떤 시퀀스를 입력으로 넣었을 때 출력으로  
또 다른 시퀀스 또는 행렬을 주는 RNN이다.

#### dropout layer
@param_1 삭제해야 하는 비율, 무작위 결정 노드 비율  

-------------------------------------------------
모델을 학습시킬 때 오버피팅이 되는 것을 방지하는 방법  
  - 모든 뉴런으로 학습하는 것이 아니라 무작위로 학습에 쓸 뉴런을
  정해서 학습을 진행
  - mini-batch 마다 랜덤으로 뉴런이 달라지기 때문에 다양한 모델을 쓰는 듯한 효과

#### Dense layer 또는 Fully connected layer  
@param_1 layer의 노드 수  

-----------------------
이전 layer의 모든 뉴런과 결합된 형태의 layer

#### Activation layer  
@param_1 layer의 노드 수  

-----------------------
신경망이 노드의 출력을 계산하는데 사용할 활성화 기능을 결정

- model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    - 각 학습의 반복에 대한 손실을 계산하기 위해 
    categorical_crossentropy(범주형 크로스 엔트로피)를 사용
        - categorical_crossentropy : 각 출력은 단 1개의 클래스에만 속해야 하지만
        2개 이상의 클래스를 가지기 때문?(to do)
    - 네트워크를 최적화 시키기 위해 RMSprop optimizer를 사용
        - RMSprop optimizer : 일반적으로 RNN에 적합

#### model.fit()
@param_1 입력 시퀀스 목록  
@param_2 각 출력의 목록  
@param_3 batch_size 샘플을 포함한 각 batch에 대해  
@param_4 epochs 설정된 횟수 동안 네트워크를 학습  

----------------------------------------------
신경망을 학습하는데 사용

#### ModelCheckpoint()
매 epoch마다 네트워크 노드의 가중치를 파일에 저장할 수 있음.  
가중치를 잃어 버릴 걱정 없이 손실값에 만족하면 학습을 멈출 수 있음.  
*ModelCheckpoint()가 없으면 200 epochs가 전부 끝날 때까지 기다려야 함.*
```python
checkpoint = ModelCheckpoint()
callbacks_list = [checkpoint]
callbacks = callbacks_list
```
학습한 것을 잃지 않고 학습을 중단시킬 수 있도록 ModelCheckpoint()를 사용


