# Base image
FROM debian:12

# Install dependencies
RUN apt-get update && apt-get install -y wget bzip2 && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/miniconda && \
    rm /tmp/miniconda.sh

# Add conda to PATH
ENV PATH="/opt/miniconda/bin:${PATH}"
