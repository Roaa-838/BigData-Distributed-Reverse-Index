# The Digital Librarian — Distributed Reverse Indexing

**Big Data Analytics | Mini Project 1**  
**Team:** Roaa Raafat (202202079) & Rana Waleed (202201737)

---

## Project Overview

This project implements a **Distributed Reverse Index** using Hadoop MapReduce and Python Streaming across a corpus of 10 public-domain books (~16 MB). It transforms slow sequential text scanning into an instant keyword lookup by building a word-to-document index in the format:

```
word --> document_a.txt:frequency, document_b.txt:frequency, ...
```

---

## Repository Contents

| File | Description |
|------|-------------|
| `mapper.py` | Tokenizes text, removes stop-words, emits (word, filename) pairs |
| `combiner.py` | Local pre-aggregation to reduce shuffle phase network I/O |
| `reducer.py` | Aggregates counts and formats the final reverse index output |
| `job.sh` | Hadoop Streaming job runner script |
| `stopwords.txt` | Common English stop-words filtered before indexing |

---

## Requirements

- Docker + Docker Compose
- Hadoop cluster (bde2020/hadoop 3.2.1 images)
- Python 3 installed inside the namenode container

---

## Setup & Execution

### Step 1 — Start the Hadoop Cluster
```bash
cd ~/hadoop-cluster
sudo docker compose up -d
```

### Step 2 — Download the Dataset (10 books from Project Gutenberg)
```bash
mkdir -p ~/gutenberg_library && cd ~/gutenberg_library
wget -O moby_dick.txt https://www.gutenberg.org/cache/epub/2701/pg2701.txt
wget -O war_and_peace.txt https://www.gutenberg.org/cache/epub/2600/pg2600.txt
wget -O count_of_monte_cristo.txt https://www.gutenberg.org/cache/epub/1184/pg1184.txt
wget -O les_miserables.txt https://www.gutenberg.org/cache/epub/135/pg135.txt
wget -O crime_and_punishment.txt https://www.gutenberg.org/cache/epub/2554/pg2554.txt
wget -O dracula.txt https://www.gutenberg.org/cache/epub/345/pg345.txt
wget -O frankenstein.txt https://www.gutenberg.org/cache/epub/84/pg84.txt
wget -O pride_and_prejudice.txt https://www.gutenberg.org/cache/epub/1342/pg1342.txt
wget -O tale_of_two_cities.txt https://www.gutenberg.org/cache/epub/98/pg98.txt
wget -O great_expectations.txt https://www.gutenberg.org/cache/epub/1400/pg1400.txt
```

### Step 3 — Load Dataset into HDFS
```bash
sudo docker cp ~/gutenberg_library namenode:/gutenberg_library
sudo docker exec -it namenode /bin/bash

hdfs dfsadmin -safemode leave
hdfs dfs -mkdir -p /user/student/library/
hdfs dfs -put /gutenberg_library/*.txt /user/student/library/
```

### Step 4 — Clone and Run
```bash
# Inside the namenode container:
git clone https://github.com/Roaa-838/BigData-Distributed-Reverse-Index.git
cd BigData-Distributed-Reverse-Index
chmod +x mapper.py reducer.py combiner.py job.sh

# Run the job (use 'time' to measure execution time)
time ./job.sh
```

---

## Scaling for Performance Experiments

To test with different cluster sizes, control NodeManagers from outside the container:

```bash
# 1 NodeManager (baseline T1)
sudo docker stop nodemanager2

# 2 NodeManagers (T2)
sudo docker start nodemanager2

# 3 NodeManagers (T3) — add nodemanager3 to docker-compose.yml first
sudo docker compose up -d
```

Always clear the output before each run (job.sh does this automatically).

---

## Performance Results

| Configuration | Execution Time | Speedup |
|---------------|---------------|---------|
| 1 NodeManager (T1) | 36.702s | 1.000 |
| 2 NodeManagers (T2) | 46.384s | 0.791 |
| 3 NodeManagers (T3) | 43.827s | 0.837 |

Sub-linear speedup is expected in a single-machine Docker environment — see the full report for Amdahl's Law analysis.

---

## Sample Output

```
whale --> moby_dick.txt:1226, frankenstein.txt:2
captain --> moby_dick.txt:538, dracula.txt:12, tale_of_two_cities.txt:3
love --> pride_and_prejudice.txt:311, les_miserables.txt:289, war_and_peace.txt:201
```
