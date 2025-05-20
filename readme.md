# Problem Based Learning: Apache Kafka

| Nama | Muhammad Andrean Rizq Prasetio |
| NRP | 5027231052 |


---

## 🗂️ Struktur Direktori Project

kafka-producers/
├─ producer_suhu.py
├─ producer_kelembaban.py
└─ spark-streaming/
├─ consumer_filter.py
└─ consumer_join.py


---

# ▶️ Cara Menjalankan (6 Terminal)

### Terminal 1: Start Zookeeper
```bash
cd ~/kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### Terminal 2: Start Kafka Broker
```bash
cd ~/kafka
bin/kafka-server-start.sh config/server.properties
```

##  Langkah 1 — Buat Topik Kafka

Untuk menerima data dari dua jenis sensor secara real-time, kita perlu membuat dua topik di Apache Kafka:

- `sensor-suhu-gudang` → untuk menampung data suhu
- `sensor-kelembaban-gudang` → untuk menampung data kelembaban

###  Perintah Membuat Topik

Jalankan perintah berikut di terminal setelah Kafka berjalan:

```bash
# Masuk ke folder Kafka
cd ~/kafka

# Buat topik untuk sensor suhu
bin/kafka-topics.sh --create \
  --topic sensor-suhu-gudang \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

# Buat topik untuk sensor kelembaban
bin/kafka-topics.sh --create \
  --topic sensor-kelembaban-gudang \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

Penjelasan Opsi
--topic: nama topik yang ingin dibuat

--bootstrap-server: alamat broker Kafka (biasanya localhost:9092 saat lokal)

--partitions 1: satu partisi cukup untuk simulasi ini

--replication-factor 1: satu replika cukup karena tidak ada cluster

Jika berhasil, terminal akan menampilkan:

```
Created topic sensor-suhu-gudang.
Created topic sensor-kelembaban-gudang.
```
