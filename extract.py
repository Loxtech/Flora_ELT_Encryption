import os
import requests

def extract_data(url: str, input_dir: str, header_line: str) -> str:
    """
    Henter flora-data fra en HTTPS-kilde og gemmer det lokalt.
    
    SIKKERHED & RELEKSION:
    1. Command Injection: Metoden anvender ren Python-netværksstak (requests) 
       og eksekverer ingen shell-kommandoer. Dermed er command injection umuligt.
    2. HTTPS: Kryptering og SSL-certifikatvalidering håndteres automatisk under transport.
    3. Robusthed: Ved at sætte 'stream=True' og læse via 'iter_content(chunk_size=1024)' 
       hentes data i små blokke. Det forhindrer RAM-overbelastning ved store filer.
    """
    # Træk filnavnet ud fra URL'en (f.eks. 'iris.csv') uden hardcoding
    filename = os.path.basename(url)
    filepath = os.path.join(input_dir, filename)
    
    # Hent data som en stream over HTTPS
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()  # Kaster en fejl hvis HTTP-status ikke er 200 OK
    
    # Gem data lokalt
    with open(filepath, 'wb') as f:
        # Skriv kolonnenavne som første linje
        f.write((header_line + '\n').encode('utf-8'))
        
        # Stream data i små blokke (1 KB ad gangen)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                
    return filepath