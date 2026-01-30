from scapy.all import *
import smtplib
from email.mime.text import MIMEText
import time
from collections import defaultdict

# --- CONFIGURATION EMAIL ---
EMAIL_SOURCE = "tonemail@gmail.com"
EMAIL_MOT_DE_PASSE = "tonpassword"
EMAIL_DESTINATION = "tonemail@gmail.com"

# --- PARAMÈTRES DE DÉTECTION ---
SEUIL_SYN = 15          # Nombre de paquets SYN autorisés
FENETRE_TEMPS = 5       # Fenêtre de temps en secondes

# --- SUIVI DES ACTIVITÉS ---
suivi_syn = defaultdict(list)
ips_deja_alertees = []  # Anti-spam email

def envoyer_alerte(sujet, message):
    email = MIMEText(message)
    email["Subject"] = f"[IDS ALERT] {sujet}"
    email["From"] = EMAIL_SOURCE
    email["To"] = EMAIL_DESTINATION

    try:
        serveur = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        serveur.login(EMAIL_SOURCE, EMAIL_MOT_DE_PASSE)
        serveur.send_message(email)
        serveur.quit()
        print(f"--> Alerte envoyée : {sujet}")
    except Exception as erreur:
        print(f"Erreur lors de l'envoi de l'email : {erreur}")

def analyser_paquet(paquet):
    # On analyse uniquement le TCP sur IP
    if paquet.haslayer(TCP) and paquet.haslayer(IP):
        ip_source = paquet[IP].src
        port_destination = paquet[TCP].dport
        drapeaux = paquet[TCP].flags

        # 1. DÉTECTION XMAS SCAN (FIN + PSH + URG)
        # Valeur hexadécimale : 0x29
        if drapeaux == 0x29:
            print(f"[!] XMAS SCAN DÉTECTÉ depuis {ip_source}")
            if ip_source not in ips_deja_alertees:
                envoyer_alerte(
                    "XMAS Scan détecté",
                    f"L'adresse IP {ip_source} envoie des paquets TCP Xmas."
                )
                ips_deja_alertees.append(ip_source)

        # 2. DÉTECTION NULL SCAN (aucun flag)
        elif drapeaux == 0x00:
            print(f"[!] NULL SCAN DÉTECTÉ depuis {ip_source}")
            if ip_source not in ips_deja_alertees:
                envoyer_alerte(
                    "NULL Scan détecté",
                    f"L'adresse IP {ip_source} envoie des paquets TCP sans flags."
                )
                ips_deja_alertees.append(ip_source)

        # 3. DÉTECTION SYN FLOOD / PORT SCAN
        # Flag SYN seul = 0x02
        elif drapeaux == 0x02:
            temps_actuel = time.time()
            suivi_syn[ip_source].append(temps_actuel)

            # Nettoyage de la fenêtre glissante
            suivi_syn[ip_source] = [
                t for t in suivi_syn[ip_source]
                if temps_actuel - t < FENETRE_TEMPS
            ]

            if len(suivi_syn[ip_source]) > SEUIL_SYN:
                print(
                    f"[!] PORT SCAN DÉTECTÉ depuis {ip_source} "
                    f"({len(suivi_syn[ip_source])} paquets / {FENETRE_TEMPS}s)"
                )
                if ip_source not in ips_deja_alertees:
                    envoyer_alerte(
                        "Scan de ports détecté",
                        f"L'adresse IP {ip_source} effectue un scan agressif."
                    )
                    ips_deja_alertees.append(ip_source)

print("[*] RedAlert-Pi lancé. Surveillance réseau active...")
sniff(filter="tcp", prn=analyser_paquet, store=0)
