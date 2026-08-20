import os
import requests
import subprocess
import urllib.request

# Requests
def extract_data_requests(data_url: str, input_dir: str, header_line: str) -> str:
    """
    Fordele:
    - Kører rent i Pythons eget netværkslag (udføres aldrig i systemets shell).
    - 100% beskyttet mod Command Injection.
    - Anvender stream=True for at undgå at fylde RAM ved store filer.
    """
    os.makedirs(input_dir, exist_ok=True)
    filename = os.path.basename(data_url)
    filepath = os.path.join(input_dir, filename)

    response = requests.get(data_url, stream=True)
    response.raise_for_status()

    with open(filepath, "w", encoding="utf-8") as f:
        # Tilføj header hvis den mangler i rådata
        f.write(f"{header_line}\n")
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                f.write(chunk)

    return filepath

# wget (urllib.request).
def extract_data_wget(data_url: str, input_dir: str, header_line: str) -> str:
    """
    Sikkerhedsadvarsel:
    - 'urllib' er indbygget i Python, men håndterer ikke streaming eller komplekse 
      HTTPS-certifikater og retries lige så robust som 'requests'.
    """
    os.makedirs(input_dir, exist_ok=True)
    filename = os.path.basename(data_url)
    filepath = os.path.join(input_dir, filename)

    # Henter rådata til en midlertidig fil
    temp_filepath = os.path.join(input_dir, f"temp_{filename}")
    urllib.request.urlretrieve(data_url, temp_filepath)

    # Indsæt header og sammensæt den endelige fil
    with open(temp_filepath, "r", encoding="utf-8") as src, open(filepath, "w", encoding="utf-8") as dst:
        dst.write(f"{header_line}\n")
        dst.write(src.read())

    # Fjern midlertidig fil
    if os.path.exists(temp_filepath):
        os.remove(temp_filepath)

    return filepath

# Subprocess/cURL.
def extract_data_subprocess(data_url: str, input_dir: str, header_line: str) -> str:
    """
    Sikkerhedsadvarsel:
    - Kalder eksterne OS-binærer via operativsystemet.
    - Kan udgøre en sikkerhedsrisiko (Command Injection), hvis data_url eller parametre 
      kommer fra ubetroede kilder og køres med shell=True.
    - Afhænger af, at cURL er installeret på værtsoperativsystemet (Linux/WSL).
    """
    os.makedirs(input_dir, exist_ok=True)
    filename = os.path.basename(data_url)
    filepath = os.path.join(input_dir, filename)

    # Eksekverer cURL som en ekstern proces uden brug af shell=True for bedre sikkerhed
    temp_filepath = os.path.join(input_dir, f"temp_curl_{filename}")
    subprocess.run(["curl", "-s", "-o", temp_filepath, data_url], check=True)

    # Indsæt header og gem til endelig fil
    with open(temp_filepath, "r", encoding="utf-8") as src, open(filepath, "w", encoding="utf-8") as dst:
        dst.write(f"{header_line}\n")
        dst.write(src.read())

    if os.path.exists(temp_filepath):
        os.remove(temp_filepath)

    return filepath


# Standard funktion som kaldes fra main.py
def extract_data(data_url: str, input_dir: str, header_line: str) -> str:
    # Request er brugt som standard
    return extract_data_requests(data_url, input_dir, header_line)