FROM ubuntu:16.04

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
