FROM nvcr.io/nvidia/pytorch:24.05-py3 

# Create user
RUN groupadd -g 1000 enzo && \
    useradd -u 1000 -g enzo enzo

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1 && \
    rm -rf /var/lib/apt/lists/*

# Install ultralytics
RUN pip install ultralytics
RUN pip install opencv-python --upgrade
#RUN pip install minio

USER enzo

WORKDIR /home/enzo/
