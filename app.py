import pyspark
import nltk
import emoji
import re
import psutil
import math
import os

import preprocessor as tweet_preprocesor
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, size, length, col
from pyspark.sql.types import StringType, DoubleType

from flask import Flask, jsonify, request, json

from extrafunctions import clean_text

tweet_preprocesor.set_options(
    tweet_preprocesor.OPT.ESCAPE_CHAR,
    tweet_preprocesor.OPT.URL,
    tweet_preprocesor.OPT.URL,
)

STOPWORDS = nltk.corpus.stopwords.words("english")

## Mount flask app
app = Flask(__name__)
#app.config['JSON_AS_ASCII'] = False

## Get 70% of available memory
memory = math.ceil((psutil.virtual_memory().total / (1024.0 ** 3)) * 0.7)

## Mount Spark app
spark = (
    SparkSession.builder.master("local[*]")
    .config("spark.driver.memory", f"{memory}g")
    .appName("text-preprop-spark-app")
    .getOrCreate()
)

## User defined function Spark
clean_text_udf = udf(clean_text, StringType())

## Clean text method

## Clean text method
@app.route("/clean_texts", methods=["POST"])
def clean_texts():
    texts = request.get_json()
    texts = texts["texts"]
    texts = [[a] for a in texts]
    df = spark.createDataFrame(texts, ["texts"])
    df = df.filter(length(col("texts")) > 0)
    df = df.dropDuplicates(["texts"])
    df = df.withColumn("text_clean", clean_text_udf(df["texts"]))
    cleaned_texts = list(df.select("text_clean").toPandas()["text_clean"])
    return jsonify({"cleaned_texts": cleaned_texts})


@app.route("/", methods=["GET"])
def hola():
    return jsonify({"response": "Hola!"})


@app.route("/leer", methods=["POST"])
def leer():
    texts = request.get_json()
    print(texts)
    return jsonify({"input": texts})


if __name__ == "__main__":
    try:
        app.run(debug=True, port=os.environ.get("FLASK_PORT", 8080), host="0.0.0.0")
    finally:
        spark.stop()

