FROM ubuntu:16.04

# Graphviz. The precompiled version does not support many of the options, therefore we compile it ourselfs

RUN apt-get update
RUN apt-get install -y wget
RUN wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
RUN tar -xf graphviz-2.40.1.tar.gz
RUN apt-get install -y libgts-dev
RUN apt-get install -y libatk1.0-0 libcairo2 libexpat1 libgd3 libgdk-pixbuf2.0-0 libgtk2.0-0 libgts-0.7-5 \
    liblasi-dev libltdl7 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 librsvg2-2
RUN apt-get install -y libann0 fontconfig
WORKDIR graphviz-2.40.1
RUN pkg-config --libs gts
RUN pkg-config --cflags gts
RUN ./configure --with-gts
RUN make
RUN make install

# Anaconda3
# https://hub.docker.com/r/continuumio/anaconda3/~/dockerfile/

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

# Neo4J
# https://github.com/neo4j/docker-neo4j-publish/blob/a50bed8c92cb9d24adb6b5a7353455c222b1be9d/3.1.3/community/Dockerfile

ENV NEO4J_SHA256 f0d79b4a98672dc527b708113644b8961ba824668c354e61dc4d2a16d8484880
ENV NEO4J_TARBALL neo4j-community-3.1.3-unix.tar.gz
ARG NEO4J_URI=http://dist.neo4j.org/neo4j-community-3.1.3-unix.tar.gz

RUN curl --fail --silent --show-error --location --remote-name ${NEO4J_URI} \
    && echo "${NEO4J_SHA256}  ${NEO4J_TARBALL}" | sha256sum -cw - \
    && tar --extract --file ${NEO4J_TARBALL} --directory /var/lib \
    && mv /var/lib/neo4j-* /var/lib/neo4j \
    && rm ${NEO4J_TARBALL}

WORKDIR /var/lib/neo4j

RUN mv data /data \
    && ln -s /data

VOLUME /data

EXPOSE 7474 7473 7687

COPY src /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN apt-get install -y python3-pyqt4

ENTRYPOINT ["python", "app.py"]