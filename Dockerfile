#FROM ubuntu:16.04
FROM phusion/baseimage:0.10.1

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# build-time arguments
ARG name=rusty
RUN apt-get update
RUN useradd -c 'rusty' -m -d /home/${name} -s /bin/bash ${name}
USER ${tester_name}
ENV HOME /home/${tester_name}

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:freecad-maintainers/freecad-daily && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install freecad-daily && \
    apt-get install -y python-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# runtime environment variables
ENV PYTHONPATH /usr/lib/freecad-daily/lib
RUN pip install cadquery flask

COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]

# default run command
CMD ["app.py"]
