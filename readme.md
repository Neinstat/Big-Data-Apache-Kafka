# Problem Based Learning: Apache Kafka

| Nama    | Muhammad Andrean Rizq Prasetio |
| -------- | ------- |
| NRP  | 5027231052    |

---

##  Struktur Direktori Project

```
Big-Data-Apache-Kafka
|   producer_suhu.py
│   producer_kelembapan.py    
└───Spark-Streaming
    └───consumer_filter.py
    └───consumer_join.py
└───README.md
```

---

#  Cara Menjalankan (6 Terminal)

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
- Topic: nama topik yang ingin dibuat
- Bootstrap-server: alamat broker Kafka (biasanya localhost:9092 saat lokal)
- Partitions 1: satu partisi cukup untuk simulasi ini
- Replication-factor 1: satu replika cukup karena tidak ada cluster

Jika berhasil, terminal akan menampilkan:

```
Created topic sensor-suhu-gudang.
Created topic sensor-kelembaban-gudang.
```

---

##  Langkah 2 — Simulasikan Data Sensor (Kafka Producer)

Setiap gudang (G1, G2, G3) akan mengirimkan data **setiap detik** ke Kafka melalui dua topik berbeda:

- `sensor-suhu-gudang` → berisi data suhu
- `sensor-kelembaban-gudang` → berisi data kelembaban

###  Langkah-langkah:

1. **Jalankan producer suhu**
   -  File: `producer_suhu.py`
   - Fungsi: Mengirimkan data suhu acak (75–90°C) setiap detik dari gudang G1, G2, G3 ke Kafka.

2. **Jalankan producer kelembaban**
   -  File: `producer_kelembaban.py`
   - Fungsi: Mengirimkan data kelembaban acak (65–80%) setiap detik dari gudang G1, G2, G3 ke Kafka.

---

##  Langkah 3 — Konsumsi & Filter Data dengan PySpark

Setelah data terkirim ke Kafka, tahap berikutnya adalah mengkonsumsi data dan melakukan filtering berdasarkan ambang batas.

###  Tujuan:

- Menampilkan peringatan jika **suhu > 80°C**
- Menampilkan peringatan jika **kelembaban > 70%**

###  Langkah-langkah:

1. **Jalankan consumer PySpark untuk filtering**
   -  File: `consumer_filter.py`
   - Fungsi: Mengkonsumsi dua topik Kafka, lalu menampilkan peringatan:
     - `[Peringatan Suhu Tinggi] Gudang G2: Suhu 85°C`
     - `[Peringatan Kelembaban Tinggi] Gudang G3: Kelembaban 74%`

---

##  Langkah 4 — Join Dua Stream & Deteksi Bahaya Ganda

Langkah ini bertujuan untuk menganalisis data secara real-time dari dua sensor yang berbeda secara **terkait waktu**, agar bisa mendeteksi kondisi gudang yang kritis.

###  Tujuan:

- Lakukan join antar dua stream berdasarkan `gudang_id` dan timestamp window waktu (±10 detik)
- Tampilkan hasil analisis dengan status seperti:
  - **Aman**
  - **Suhu tinggi, kelembaban normal**
  - **Kelembaban tinggi, suhu aman**
  - **Bahaya tinggi! Barang berisiko rusak**

###  Langkah-langkah:

1. **Jalankan consumer join PySpark**
   -  File: `consumer_join.py`
   - Fungsi: Melakukan join antara dua stream Kafka (`sensor-suhu-gudang` dan `sensor-kelembaban-gudang`) lalu menampilkan output analitik ke terminal seperti:

     ```
     [PERINGATAN KRITIS]
     Gudang G1:
     - Suhu: 84°C
     - Kelembaban: 73%
     - Status: Bahaya tinggi! Barang berisiko rusak
     ```

---

Dengan menyelesaikan seluruh langkah di atas, maka simulasi sistem monitoring gudang real-time berbasis Apache Kafka & PySpark telah berhasil diimplementasikan secara lengkap.
