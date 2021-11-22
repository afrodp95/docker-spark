FROM jupyter/pyspark-notebook:python-3.9.7

WORKDIR /app
COPY app.py /app
COPY extrafunctions.py /app

RUN pip3 install install emoji tweet-preprocessor tqdm psutil flask nltk pyspark
RUN python3 -m nltk.downloader punkt -q
RUN python3 -m nltk.downloader averaged_perceptron_tagger -q
RUN python3 -m nltk.downloader stopwords -q

CMD ["python3", "app.py", "--host=0.0.0.0"]

