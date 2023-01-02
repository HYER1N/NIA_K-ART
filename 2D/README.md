# NIA K-ART 2D Image Classification

#### Data
- K-ART 2D Image Dataset

### 실행방법

##### DOCKER
도커 컨테이너가 필요한 경우, 아래 명령어를 통해 도커 이미지를 빌드합니다.
```
docker build -t {image_name} -f Dockerfile .
docker run --rm --gpus all --ipc=host {image_name}
```

##### 이미지 전처리(Image pre progress)
```
pip install -r requirements.txt
python –u nia_pre_process.py
```

- 전처리를 진행할 경로를 current_path에 적습니다.
- 이후 진행되는 과정은 폴더가 자동적으로 생성됩니다.

##### 개별 실행(Train)

```
python -W ignore imagenet.py -a se_resnet50 --data ./{데이터셋 path}/ --epoch 100 --schedule 30 60 90 --gpu-id 0,1
```

- imagenet.py: 학습에 필요한 코드 파일을 적습니다.
- se_resnet50: 학습에 필요한 모델을 적습니다.
- {데이터셋 path} : 학습할 데이터셋의 파일 경로를 적고, 지정한 데이터셋으로 학습을 진행합니다.
- epoch 100 : epoch의 수를 의미합니다.
- gpu-id 0,1 : 학습 환경에 맞는 GPU를 설정합니다.


##### 개별 실행(Test)
```
python –W ignore test.py –a se_resnet50 –data ./{데이터셋 path}/ 
--schedule 30 60 90 –gpu-id 0
```

- test.py: 학습에 필요한 코드 파일을 적습니다.
- se_resnet50: 학습에 필요한 모델을 적습니다.
- {데이터셋 path} : 학습할 데이터셋의 파일 경로를 적고, 지정한 데이터셋으로 학습을 진행합니다.
- gpu-id 0 : 학습 환경에 맞는 GPU를 설정합니다.

##### References
[Imagenet:](https://ieeexplore.ieee.org/document/5206848) Deep Learning on images for 2D Classification
