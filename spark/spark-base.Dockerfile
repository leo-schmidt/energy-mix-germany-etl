FROM cluster-base

# -- Layer: Apache Spark

ARG spark_version=3.3.2
ARG hadoop_version=3

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${spark_version}-bin-hadoop${hadoop_version} /usr/bin/ && \
    mkdir /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/logs && \
    rm spark.tgz

# Azure Hadoop jars
RUN mkdir -p /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/jars && \
    curl -L https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure/${spark_version}/hadoop-azure-${spark_version}.jar \
    -o /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/jars/hadoop-azure-${spark_version}.jar && \
    curl -L https://repo1.maven.org/maven2/com/microsoft/azure/azure-storage/8.6.6/azure-storage-8.6.6.jar \
    -o /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/jars/azure-storage-8.6.6.jar && \
    curl -L https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure-datalake/${spark_version}/hadoop-azure-datalake-${spark_version}.jar \
    -o /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/jars/hadoop-azure-datalake-${spark_version}.jar

ENV SPARK_HOME=/usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}
ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_MASTER_PORT=7077
ENV PYSPARK_PYTHON=python3

# -- Runtime

WORKDIR ${SPARK_HOME}
