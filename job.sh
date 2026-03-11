#!/bin/bash
set -e
STREAMING_JAR=$(find "$HADOOP_HOME/share/hadoop/tools/lib" -name 'hadoop-streaming*.jar' | head -n 1)

hdfs dfs -rm -r -f /user/student/output || true

hadoop jar "$STREAMING_JAR" \
    -files mapper.py,reducer.py,combiner.py,stopwords.txt \
    -mapper mapper.py \
    -combiner combiner.py \
    -reducer reducer.py \
    -input /user/student/library/*.txt \
    -output /user/student/output

hdfs dfs -cat /user/student/output/part-00000 | head -n 30
