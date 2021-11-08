FROM jjanzic/docker-python3-opencv:latest

ENV FLASK_APP="rest_api"

RUN mkdir /install
RUN mkdir /install/temp


WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD nSkins /install/nSkins 
COPY SkinMask.py /install/SkinMask.py
COPY new_api.py /install/new_api.py
COPY magickTransformer.sh /install/magickTransformer.sh
COPY rest_api.py /install/rest_api.py


ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]