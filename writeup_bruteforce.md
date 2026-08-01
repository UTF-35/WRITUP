# 🔐 BTLO — Bruteforce | Writeup

## 📋 Scenario

> Can you analyze logs from an attempted RDP bruteforce attack?
> One of our system administrators identified a large number of Audit Failure events in the Windows Security Event log.

**Fichiers fournis :**
```
BTLO_Bruteforce_Challenge.csv
BTLO_Bruteforce_Challenge.txt
```

---

## 🧠 Méthodologie

### Qu'est-ce que le protocole RDP ?

> Le protocole RDP (Remote Desktop Protocol) est un protocole de communication réseau sécurisé développé par Microsoft. Il permet aux utilisateurs de contrôler et d'utiliser des ordinateurs à distance.  
> Source : [Fortinet](https://www.fortinet.com/fr/resources/cyberglossary/remote-desktop-protocol)

---

## ❓ Questions & Réponses

### Q1 — How many Audit Failure events are there? `(Format: Count of Events)`

**Réponse : `3103`**

Utilisation de `grep` pour compter les occurrences :

```bash
grep "Audit Failure" BTLO_Bruteforce_Challenge.csv | wc -l
```

| Option | Description |
|--------|-------------|
| `grep "Audit Failure"` | Filtre les lignes contenant "Audit Failure" |
| `wc -l` | Compte le nombre de lignes retournées |

---

### Q2 — What is the username of the local account that is being targeted? `(Format: Username)`

**Réponse : `administrator`**

> Analyse du fichier `.txt` — champ `Account Name: administrator`

---

### Q3 — What is the failure reason related to the Audit Failure logs? `(Format: String)`

**Réponse : `Unknown user name or bad password`**

> Ce message est caractéristique d'une attaque bruteforce — la même requête est répétée en masse avec des identifiants différents.

---

### Q4 — What is the Windows Event ID associated with these logon failures? `(Format: ID)`

**Réponse : `4625`**

> L'Event ID 4625 correspond au refus de connexion d'un compte Windows.  
> Source : [ManageEngine](https://www.manageengine.com/fr/active-directory-audit/kb/logon-logoff-events/event-id-4625.html)

Retrouvé via analyse du fichier `BTLO_Bruteforce_Challenge.txt`.

---

### Q5 — What is the source IP conducting this attack? `(Format: X.X.X.X)`

**Réponse : `113.161.192.227`**

> Analyse du fichier `.txt` — champ `Source Network Address: 113.161.192.227`

---

### Q6 — What country is this IP address associated with? `(Format: Country)`

**Réponse : `Viet Nam`**

Lookup de l'IP via [iplocation.io](https://iplocation.io/ip/113.161.192.227)

---

### Q7 — What is the range of source ports used by the attacker? `(LowestPort-HighestPort)`

**Réponse : `49162-65534`**

Extraction de tous les ports source :

```bash
cat BTLO_Bruteforce_Challenge.txt | grep "Source Port:" > nombredeport.txt
```

| Option | Description |
|--------|-------------|
| `grep "Source Port:"` | Filtre les lignes contenant les ports source |
| `> nombredeport.txt` | Redirige le résultat dans un fichier |

---

## 🛠️ Outils utilisés

| Outil | Usage |
|-------|-------|
| `grep` / `wc` | Analyse et comptage dans les logs |
| [iplocation.io](https://iplocation.io) | Géolocalisation de l'IP attaquante |
| [ManageEngine](https://www.manageengine.com/fr/active-directory-audit/kb/logon-logoff-events/event-id-4625.html) | Référence Event ID Windows |

---

## 📚 Ressources

- [Fortinet — Qu'est-ce que RDP ?](https://www.fortinet.com/fr/resources/cyberglossary/remote-desktop-protocol)
- [ManageEngine — Event ID 4625](https://www.manageengine.com/fr/active-directory-audit/kb/logon-logoff-events/event-id-4625.html)
- [Commandes Linux](https://blog.stephane-robert.info/docs/admin-serveurs/linux/commandes/)
- [iplocation.io](https://iplocation.io)
