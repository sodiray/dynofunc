FROM python:3.7.4

WORKDIR /usr/src/dynamof

ADD ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

ADD . .

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/dynamof"

CMD [ "python", "run_test.py" ]
