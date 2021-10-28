FROM jjanzic/docker-python3-opencv:latest

ENV FLASK_APP="rest_api"
ENV MINESKIN_API_KEY="2b61ef1f512f4d073f94a2ad1aab4591ae7e840e8894c49f74a23ceedcb5b353"
ENV MINESKIN_API_SECRET="b2e0790f66dd31d936fea64988666fbae9e7b7f61ec19f2b7369ddb0bc539b44474a2abccf6ef5f86282e23508b0e211e9ca9fe0919b8da952d8f56e8725c0ae"

RUN mkdir /install
RUN mkdir /install/output
RUN mkdir /install/skins


WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD masks /install/masks
ADD images /install/images 
COPY mineskin_api.py /install/mineskin_api.py
COPY playerdb.py /install/playerdb.py
COPY rest_api.py /install/rest_api.py
COPY skin_generator_cv_tool.py /install/skin_generator_cv_tool.py


ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]