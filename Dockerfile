FROM python:3.11
ADD . /app
WORKDIR /app
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN python3 src/init_db.py
ENV FLASK_APP=src/app
CMD ["flask", "run", "-h", "0.0.0.0"]