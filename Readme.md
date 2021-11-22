# Api de pre procesamiento de texto

En este proyecto se implementa una API REST de pre procesamiento de texto usando Apache Spark como backend para la paralelización de la tarea. La arquitectura se monta usando como base una imágen que permite la ejecución de Apache Spark a través de la API para Python usando Notebooks de Jupyter [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html).

Para este proyecto se usa la imágen [jupyter/base-notebook](https://hub.docker.com/r/jupyter/base-notebook/tags/) con Python 3.9.7, Apache Spark 3.2.0 y Apache Hadoop 3.2.

Es importante tener en cuenta que la implementación es inicialmente de ejecución local y toma automáticamente el 70% de la memoria disponible en el equipo en que se ejecuta para realizar los procesamientos.

# Dependencias

Para el pre procesamiento se usan diferentes librerías de NLP y de pre procesamiento de texto, entre ellas:

* emoji
* tweet-preprocessor
* nltk 

# Pre procesamiento realizado

El pre procesamiento valida y elimina strings duplicados y con longitud cero, luego de ello elimina links y espacios de sobra. Seguido de lo anterior se reemplazan todos los caracteres especiales por punto y entrega el texto pre procesado.

# Construcción de la imágen

Para montar la imágen y dejár la API encendida pendiente de respuestas usar los siguientes comandos

```bash
cd ./docker-spark
docker build -t docker-spark .
docker run -d -p 8888:8888 -p 4040:4040 -p 4041:4041 -e FLASK_PORT=8081 --name spark-api docker-spark:latest
docker logs spark-api
```

# Consulta al Método

El método de limpieza se consulta a través del endpoint http://host:8081/clean_texts usando una petición POST y el siguiente cuerpo de entrada:

```JSON
{
    "texts":[
        "text1",
        "text2",
        ...
        "textN"
    ]
}
```

La respuesta tendrá la siguiente estructura:

```JSON
{
    "cleaned_texts":[
        "cleaned text1",
        "cleaned text2",
        ...
        "cleaned textN"
    ]
}
```
Para testear el método usando curl, guarde los textos en un json con la estructura requerida y ejecute:

```bash
# Validar si la API responde
curl http://172.17.0.2:8081/
# Metodo de limpieza
curl --header "Content-Type: application/json" --request POST --data "@input.json" http://172.17.0.2:8081/clean_texts
```

# Desmontar y liberar puertos

Para liberar archivos de la imágen de cache y los puertos usados para disponibilizar la API a través del contenedor ejecutar:

```bash
docker stop spark-api   
docker system prune --volumes
docker container prune
docker image prune --all
```