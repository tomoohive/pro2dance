FROM python:2.7.16-slim-buster

USER root

RUN apt-get update && apt-get install -yq --no-install-recommends \
    build-essential \
    ffmpeg \
    git \
    inkscape \
    jed \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    netcat \
    pandoc \
    python-dev \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-xetex \
    tk \
    unzip \
    vim \
    wget \
    gnupg \
    swig \
    python3-dev python3-pip python3-setuptools \
    python3-opencv \
    python3-tk \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install numpy \
    scipy \
    librosa \
    imageio==2.4.1 \
    moviepy \
    youtube-dl \
    requests \
    bs4 \
    matplotlib \
    visbeat \
    opencv-python

RUN python -c "import imageio; imageio.plugins.ffmpeg.download()"

RUN pip3 install argparse \
    dill \
    fire \
    matplotlib \
    numba \
    psutil \
    requests \
    scikit-image \
    scipy \
    slidingwindow \
    tqdm \
    cython 

RUN pip3 install pycocotools \
    git+https://github.com/ppwwyyxx/tensorpack.git \
    tensorflow \
    pandas