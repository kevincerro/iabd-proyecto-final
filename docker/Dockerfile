FROM python:3.9-slim-buster

WORKDIR /var/www

ENV VIRTUAL_ENV=/tmp/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000/tcp
