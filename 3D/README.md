# NIA K-ART 3D Image Classification

## Dataset

K-Art dataset 폴더 이름을 'NIA'로 변경한 후, 'data' 폴더에 넣습니다.
- K-Art dataset


### Docker


```bash
docker build --tag={image_name} {path}
docker run --rm {image_name}
```

### 환경 설정

```bash
pip install -r requirements.txt
```

### train

```bash
python examples/train_pointnet.py
```

### test

```bash
python examples/test_pointnet.py
```

### References
- [PointNet:](https://arxiv.org/abs/1612.00593) Deep Learning on Point Sets for 3D Classification and Segmentation
