# 🚨 RedAlert-Pi: A DIY Python IDS for Raspberry Pi

> *"Pour comprendre le réseau, il faut écouter ce qu'il chuchote."*

RedAlert-Pi est un Système de Détection d'Intrusion (IDS) léger et artisanal conçu pour tourner sur un Raspberry Pi 4. Contrairement aux solutions lourdes comme Snort ou Suricata, ce projet a été codé **from scratch** en Python avec Scapy pour comprendre la mécanique interne d'une cyberattaque.

Il ne se contente pas de loguer : il analyse les flags TCP en temps réel et m'envoie une alerte mail immédiate s'il détecte des anomalies (Scans Nmap, paquets malformés, flood).

---

## ⚡ Fonctionnalités

- 🕵️ **Sniffing Promiscuous** : Capture tout le trafic entrant sur l'interface
- 🧠 **Analyse Comportementale** :
  - Détection de SYN Scans (Nmap Stealth Scan)
  - Détection de XMAS Scans (Paquets "sapin de noël" illogiques)
  - Détection de NULL Scans (Paquets sans flags)
- 📧 **Alerting Temps Réel** : Exfiltration des infos de l'attaquant (IP, Port, Heure) par SMTP (Gmail)
- 🛡️ **Anti-Spam** : Système de "cooldown" pour ne pas spammer la boite mail si l'attaque persiste

---

## 🛠️ Hardware & Prérequis

- **Matériel** : Raspberry Pi 4B (8GB RAM recommandé pour le buffer réseau, mais tourne sur moins)
- **OS** : Raspberry Pi OS Lite (Headless)
- **Réseau** : Connecté en Ethernet (eth0) sur le switch principal
- **Langage** : Python 3 + droits Root

---

## 📖 Deep Dive : Comment ça marche ?

L'objectif de ce projet n'était pas juste d'installer un outil, mais d'implémenter la logique de détection. Voici comment le script analyse la "matrice".

### 1. L'anatomie d'une attaque (TCP Flags)

Pour détecter une intrusion, on regarde les drapeaux (Flags) de l'en-tête TCP.  
Le script isole trois types de comportements anormaux :

#### A. Le SYN Scan (Le classique)

Un attaquant (Nmap) veut savoir quels ports sont ouverts sans établir de connexion complète (pour être discret).

- **Normal** : `SYN -> SYN/ACK -> ACK` (Connexion établie)
- **Attaque** : `SYN -> SYN/ACK -> RST` (L'attaquant coupe court)

**La détection** : Si je reçois une avalanche de paquets SYN (Flag S) provenant de la même IP en moins de quelques secondes, c'est un scan.

#### B. Le XMAS Scan (Le "Bizarre")

L'attaquant envoie un paquet avec les flags **FIN, URG, et PSH** allumés en même temps.

**Pourquoi ?** C'est illogique selon le protocole TCP. Certains vieux OS plantent ou répondent différemment, trahissant leur présence.

**La détection** : `if packet[TCP].flags == 0x29` (FIN+PSH+URG). Un paquet légitime ne ressemble jamais à ça.

#### C. Le NULL Scan (Le fantôme)

L'attaquant envoie un paquet avec **aucun flag activé**.

**La détection** : `if packet[TCP].flags == 0`. Cela n'arrive jamais dans une communication normale.

### 2. L'implémentation (Scapy)

On utilise `sniff()` de Scapy qui agit comme un aspirateur à paquets. Chaque paquet passe dans une fonction de tri (`packet_callback`) qui applique les règles ci-dessus.
```python
# Exemple de logique simplifiée
if packet[TCP].flags == "S":  # C'est un SYN
    track_ip(packet[IP].src)  # On incrémente le compteur de cette IP
    if count > SEUIL:
        ALERTE()
```

---

## 🚀 Installation & Utilisation

### 1. Cloner le repo & Dépendances
```bash
git clone https://github.com/tonuser/RedAlert-Pi.git
cd RedAlert-Pi
sudo apt update && sudo apt install python3-pip
pip3 install scapy
```

### 2. Configuration

Editez le fichier `ids.py` pour ajouter vos identifiants mail (utilisez un mot de passe d'application pour Gmail) :
```python
# ids.py
MAIL_USER = "votre_mail@gmail.com"
MAIL_PASS = "votre_mot_de_passe_app"
INTERFACE = "eth0"
```

### 3. Lancer l'IDS

Le script a besoin de droits root pour mettre la carte réseau en mode écoute.
```bash
sudo python3 ids.py
```

Vous devriez voir :
```
[*] Initialisation du moteur de détection...
[*] Interface eth0 en mode PROMISCUOUS.
[*] En attente de paquets suspects...
```

---

## 🧪 Proof of Concept (Test d'intrusion)

Pour vérifier que le Raspberry Pi surveille bien le réseau, j'ai lancé une attaque depuis mon laptop (Kali Linux) situé sur le même LAN.

**Commande de l'attaquant :**
```bash
# Scan agressif Xmas sur le Pi
sudo nmap -sX -p- 192.168.1.55
```

**Logs du Raspberry Pi (IDS) :**
```
[!] Paquet suspect détecté : XMAS SCAN
[+] Source : 192.168.1.14 -> Destination : 192.168.1.55
[+] Flags TCP : FPU (0x29)
[!!!] ALERTE ENVOYÉE PAR MAIL.
```

**Résultat Mail :**  
Je reçois instantanément une notification sur mon téléphone m'avertissant que l'IP `192.168.1.14` tente des manipulations exotiques sur le réseau.

---

## 📝 License

MIT

## 🤝 Contributions

Les PRs sont les bienvenues ! N'hésitez pas à ouvrir une issue pour discuter de nouvelles détections.
