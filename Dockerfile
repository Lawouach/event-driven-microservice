FROM python:3.5.1
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/usr/local/app
COPY bookshelf /usr/local/app/bookshelf
ENTRYPOINT [ "python"]