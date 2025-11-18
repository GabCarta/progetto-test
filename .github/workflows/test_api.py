import requests
import sys

# --- Configurazione ---
BASE_URL = 'http://localhost:8000'

# !!! IMPORTANTE !!!
# Sostituisci questo con un TOKEN VERO E VALIDO ottenuto
# dal tuo microservizio di autenticazione (es. dopo un login)
AUTH_TOKEN = 'METTI_IL_TUO_TOKEN_QUI' 

# Creiamo gli headers che useremo per le richieste autenticate
AUTH_HEADERS = {
    'Authorization': f'Bearer {AUTH_TOKEN}',
    'Content-Type': 'application/json'
}

# ==========================================================
# 1. TEST: Recuperare tutti i thoughts (GET)
# ==========================================================
print("--- 1. Esecuzione Test GET (Recupero thoughts) ---")
try:
    get_url = f'{BASE_URL}/thoughts/'
    response_get = requests.get(get_url)

    if response_get.status_code == 200:
        print(f"GET OK (200): Richiesta riuscita.")
        print("Risposta JSON:", response_get.json())
    else:
        print(f"Errore GET: Status {response_get.status_code}")
        print("Risposta:", response_get.text)

except requests.exceptions.ConnectionError:
    print(f"ERRORE CONNESSIONE: Impossibile raggiungere {BASE_URL}.")
    print("Assicurati che 'docker compose up' sia attivo.")
    sys.exit(1)
except Exception as e:
    print(f"Errore generico GET: {e}")


print("\n" + "="*40 + "\n") # Separatore


# ==========================================================
# 2. TEST: Creare un nuovo thought (POST)
# ==========================================================
print("--- 2. Esecuzione Test POST (Creazione thought) ---")

post_url = f'{BASE_URL}/thoughts/'
post_data = {
    'username': 'mario',
    'text': 'Ciao, questo è un test con POST!'
}

try:
    response_post = requests.post(post_url, headers=AUTH_HEADERS, json=post_data)

    # 201 Created è lo status code standard per un POST riuscito
    if response_post.status_code == 201:
        print("POST OK (201 Created): Nuovo thought creato!")
        print("Risposta JSON:", response_post.json())
    
    # Gestiamo i comuni errori di autenticazione
    elif response_post.status_code == 401 or response_post.status_code == 403:
        print(f"Errore POST: Status {response_post.status_code} (Unauthorized/Forbidden)")
        print("PROBLEMA: Il token non è valido, è scaduto o non hai i permessi.")
        print("Verifica la stringa 'AUTH_TOKEN' nello script.")
        print("Risposta:", response_post.text)
    
    # Altri errori (es. 400 Bad Request, 500 Server Error)
    else:
        print(f"Errore POST: Status {response_post.status_code}")
        print("Risposta:", response_post.text)

except requests.exceptions.ConnectionError:
    print(f"ERRORE CONNESSIONE: Impossibile raggiungere {post_url}.")
    sys.exit(1)
except Exception as e:
    print(f"Errore generico POST: {e}")