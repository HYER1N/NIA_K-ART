
# FROM nvidia/cuda:11.1.1-devel-ubuntu18.04
# FROM nvidia/cuda:11.0.3-devel-ubuntu18.04
FROM nvidia/cuda:11.4.1-runtime-ubuntu18.04


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH


RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
	    git \
	    curl \
        libglib2.0-0 \
        software-properties-common \
        python3-pip


# Install Dependencies of Miniconda
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    # /opt/conda/bin/conda clean -tipsy && \ 
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc 

WORKDIR /home/user/SSD/nia/nia_docker/

# 가상환경
COPY environment.yaml   /home/user/SSD/nia/nia_docker/
RUN conda env create -f environment.yaml

ENV CODNA_DEFAULT_ENV $nia


COPY checkpoint.pth.tar   /home/user/SSD/nia/nia_docker/
COPY *.py   /home/user/SSD/nia/nia_docker/
COPY dataset_test   /home/user/SSD/nia/nia_docker/dataset_test
COPY models   /home/user/SSD/nia/nia_docker/models
COPY utils   /home/user/SSD/nia/nia_docker/utils


ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "nia", "python", "-W", "ignore", "test.py", "-a", "se_resnet50", "--data", "./dataset_test/", "--schedule", "30", "60", "90","--gpu-id", "0"]
