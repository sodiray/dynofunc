FROM python:3.7.4

WORKDIR /usr/src/idynamo

ADD ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

ADD . .

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/idynamo"

CMD [ "python", "run_test.py" ]
