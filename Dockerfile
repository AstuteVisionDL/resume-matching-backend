FROM nvidia/cuda:12.3.1-base-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.10 python3-pip

RUN python3 -m pip install --no-cache-dir --upgrade pip

ARG REF=main

# If set to nothing, will install the latest version
ARG PYTORCH='2.1.0'
ARG TORCH_VISION=''
ARG TORCH_AUDIO=''
# Example: `cu102`, `cu113`, etc.
ARG CUDA='cu121'

RUN [ ${#PYTORCH} -gt 0 ] && VERSION='torch=='$PYTORCH'.*' ||  VERSION='torch'; python3 -m pip install --no-cache-dir -U $VERSION --extra-index-url https://download.pytorch.org/whl/$CUDA
RUN [ ${#TORCH_VISION} -gt 0 ] && VERSION='torchvision=='TORCH_VISION'.*' ||  VERSION='torchvision'; python3 -m pip install --no-cache-dir -U $VERSION --extra-index-url https://download.pytorch.org/whl/$CUDA
RUN [ ${#TORCH_AUDIO} -gt 0 ] && VERSION='torchaudio=='TORCH_AUDIO'.*' ||  VERSION='torchaudio'; python3 -m pip install --no-cache-dir -U $VERSION --extra-index-url https://download.pytorch.org/whl/$CUDA

# Upgrade pip to the latest version
RUN python3 -m pip install --no-cache-dir --upgrade pip
WORKDIR /app
RUN pip install poetry
ADD poetry.lock .
ADD pyproject.toml .
RUN poetry config installer.max-workers 10
RUN poetry install
COPY /src ./src