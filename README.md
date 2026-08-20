# Flora ELT & Encryption Pipeline

En udvidet databehandlingspipeline i Python, der overfører, transformerer og gemmer Iris-datasetmålinger sikkert ved hjælp af AES-symmetrisk kryptering (Fernet) for data at rest.

---

## 📌 Projektets Formål & Ændringer i Iteration 2

Projektet bygger videre på den oprindelige ELT-pipeline og tilføjer et stærkt sikkerhedslag for data at rest (*Data at Rest Encryption*):

1. **Sikkerhed at Rest (AES / Fernet):** 
   - Alle numeriske målinger og artsnavne krypteres inden lagring i både CSV og MySQL.
   - Der anvendes **Fernet** (symmetrisk 128-bit AES med HMAC-SHA256 dataintegritetskontrol) via `cryptography`-biblioteket.
2. **Database-koeksistens:** 
   - Krypterede data gemmes i en separat database-tabel, `iris_setosa_encrypted`, så den eksisterende arv-tabel (`iris_setosa`) ikke overskrives.
3. **Dekryptering ved Visualisering:** 
   - Visualiseringsmodulet henter de krypterede data ud af MySQL, dekrypterer dem i memory og konverterer dem tilbage til numeriske typering (`float`) før graferne genereres.
4. **Fleksibel Extractor:** 
   - Udover den primære `requests`-baserede extractor indeholder modulet nu demonstrative metoder for `urllib`/`wget` og `subprocess/cURL`.

---

## 🛠️ Modulopdeling

Pipelinens kodebase er modulær og opdelt i følgende Python-filer:

* **`main.py`**: Pipelinedirektør og orkestrering af de fire faser.
* **`security.py`**: Håndterer generering/indlæsning af nøglen (`secret.key`) samt kryptering (`encrypt_val`) og dekryptering (`decrypt_val`).
* **`extract.py`**: Henter rådata fra netværket. Indeholder `extract_data_requests` (foretrukket), `extract_data_wget` og `extract_data_subprocess`.
* **`transform.py`**: Initialiserer PySpark, tilføjer skema-headers og filtrerer på `Iris-setosa`.
* **`load.py`**: Konverterer PySpark DataFrames til Pandas (via `.collect()` for at undgå Py4J-konflikter), krypterer datasættet celleniveau-vis og gemmer til CSV og MySQL.
* **`visualize.py`**: Henter krypterede data fra MySQL, kører dekryptering og typekonvertering samt genererer tre visuelle grafer.

---

## 🔐 Sikkerhed & Best Practices

* **Secret Key Management:** Nøglen genereres automatisk i `secret.key`. Denne fil indeholder master-dekrypteringsnøglen og er tilføjet til `.gitignore`, så den aldrig uploades til GitHub.
* **Command Injection Protection:** Dataindlæsningen sker som standard via Pythons `requests`-bibliotek i Pythons eget netværkslag for at undgå at tilgå operativsystemets shell.

---

## Systemkrav

For at køre projektet skal din maskine have følgende installeret:

1. **Python 3.10+**
2. **Java Runtime Environment (JRE / JDK 8+)** (påkrævet af PySpark til Java-motoren)
3. **MySQL Server** (kørende lokalt)

---

## Trin-for-trin Instruktioner

### 1. Kloning af repository
Åbn din terminal og klon projektet fra GitHub:

```bash
git clone https://github.com/Loxtech/Flora_ELT_Encryption.git
cd flora-etl_Encryption
```

### 2. Opret og aktiver virtuelt miljø
Opret et isoleret Python-miljø og aktiver det:

```bash
python3 -m venv .venv
source ../.venv/bin/activate
```

### 3. Installer afhængigheder
Installer alle nødvendige Python-biblioteker:

```bash
pip install pyspark pandas sqlalchemy pymysql requests cryptography matplotlib seaborn
```

### 4. Konfigurer og start MySQL
Sørg for, at MySQL-tjenesten kører på din maskine:

```bash
sudo service mysql start
```

Forbindelsesoplysningerne i `main.py` er sat op til følgende standardindstillinger:
* **Host:** `127.0.0.1`
* **Port:** `3306`
* **User:** `root`
* **Password:** `password`
* **Database:** `flora_db` *(oprettes automatisk af koden, hvis den mangler)*

Hvis din MySQL root-bruger kræver adgangskodeopsætning, kan du sætte den inde i MySQL med:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
FLUSH PRIVILEGES;
```

---

## Kørsel af applikationen

Når det virtuelle miljø er aktivt og MySQL kører, afvikles hele pipelinen med kommandoen:

```bash
python3 main.py
```

---

## Output og Resultater

Når programmet har fuldført kørslen, vil følgende resultater være genereret:

1. **CSV-fil**: `Output_dir/transformed_iris.csv` (indeholder kun målinger for *Iris-setosa*).
2. **MySQL Tabelle** iris_setosa_encrypted: **Databasetabel med det krypterede datasæt**`.
3. secret.key : **Fernet-nøglen brugt til kryptering og dekryptering.**
4. Output_dir/transformed_iris.csv: **En CSV-fil hvor alle felter fremstår som Base64-krypterede strenge.**
3. **Grafiske visualiseringer**:
   * `Output_dir/scatter_plot.png` (Sepal Length vs Petal Length)
   * `Output_dir/histogram.png` (Fordeling af Petal Width)
   * `Output_dir/boxplots.png` (Boxplots for alle fire målinger)