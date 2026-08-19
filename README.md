# Flora ETL Pipeline

Dette projekt er en modulær ETL-pipeline (Extract, Transform, Load) opbygget i Python. Pipelinen henter Iris-datasættet, filtrerer og transformerer data for arten *Iris-setosa* ved hjælp af PySpark, gemmer resultaterne i en CSV-fil samt en MySQL-database, og genererer datavisualiseringer med Pandas og Seaborn.

---

## Projektstruktur

Projektet er opdelt i moduler efter ETL-principperne:

* **`main.py`**: Hovedscriptet der styrer hele ETL-forløbet og afviklingen.
* **`extract.py`**: Henter rådata (`iris.csv`) direkte fra GitHub via PySpark.
* **`transform.py`**: Renser data, tilføjer kolonnenavne og filtrerer på `species == 'Iris-setosa'`.
* **`load.py`**: Konverterer data og gemmer det i en ny CSV-fil samt i en MySQL-database.
* **`visualize.py`**: Henter data fra MySQL og genererer grafer (Scatterplot, Histogram og Boxplots).
* **`Output_dir/`**: Mappe hvor den transformerede CSV-fil og graferne gemmes.

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
git clone https://github.com/Loxtech/flora-etl.git
cd flora-etl
```

### 2. Opret og aktiver virtuelt miljø
Opret et isoleret Python-miljø og aktiver det:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer afhængigheder
Installer alle nødvendige Python-biblioteker:

```bash
pip install pyspark pandas sqlalchemy pymysql matplotlib seaborn
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
2. **MySQL Database**: Databasen `flora_db` indeholdende tabellen `iris_setosa`.
3. **Grafiske visualiseringer**:
   * `Output_dir/scatter_plot.png` (Sepal Length vs Petal Length)
   * `Output_dir/histogram.png` (Fordeling af Petal Width)
   * `Output_dir/boxplots.png` (Boxplots for alle fire målinger)