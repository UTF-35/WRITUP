# 🔐 BTLO — Secrets | JWT Challenge Writeup

## 📋 Scenario

> You're a senior cyber security engineer. During your shift, a high privilege action from an unknown source has been intercepted. You have been given the ticket that made these actions. You are the one who created the secret for these tickets. Fix this and submit the low privilege ticket.

**Token intercepté :**
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOnRydWV9.jbkZHll_W17BOALT95JQ17glHBj9nY-oWhT1uiahtv8
```

---

## 🧠 Méthodologie

### Qu'est-ce qu'un JWT ?

> JSON Web Token est un standard ouvert défini dans la RFC 7519. Il permet l'échange sécurisé de jetons entre plusieurs parties, via HMAC ou RSA.  
> Source : [Wikipedia](https://fr.wikipedia.org/wiki/JSON_Web_Token)

**Structure :**
```
Header.Payload.Signature
xxxxx.yyyyy.zzzzz
```

- **Header** — algorithme de signature
- **Payload** — données (claims)
- **Signature** — intégrité du token, calculée avec le secret

> Un token JWT commence toujours par `eyJ` — c'est `{"` encodé en Base64URL, avec exactement 2 points `.` séparant les 3 parties.

---

## ❓ Questions & Réponses

### Q1 — Can you identify the name of the token? `(Format: String)`

**Réponse : `JWT`**

Le token commence par `eyJ` et suit la structure `Header.Payload.Signature` — c'est le format JSON Web Token.

---

### Q2 — What is the structure of this token? `(Format: Section.Section.Section)`

**Réponse : `Header.Payload.Signature`**

Décodage du token via [CyberChef](https://gchq.github.io/CyberChef/#recipe=JWT_Decode()&input=ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5Sm1iR0ZuSWpvaVFsUk1lMTgwWDBWNVpYTjlJaXdpYVdGMElqbzVNREF3TURBd01Dd2libUZ0WlNJNklrZHlaV0YwUlhod0lpd2lZV1J0YVc0aU9uUnlkV1Y5Lmpia1pIbGxfVzE3Qk9BTFQ5NUpRMTdnbEhCajluWS1vV2hUMXVpYWh0djg) :

```json
// Header
{"typ":"JWT","alg":"HS256"}

// Payload
{"flag":"BTL{_4_Eyes}","iat":90000000,"name":"GreatExp","admin":true}
```

---

### Q3 — What is the hint you found from this token? `(Format: String)`

**Réponse : `_4_Eyes`**

Dans le payload, un champ non-standard `flag` contient `BTL{_4_Eyes}`. C'est un flag CTF embarqué directement dans le token — le hint est la valeur entre accolades.

---

### Q4 — What is the Secret? `(Format: String)`

**Réponse : `bT!0`**

Le secret a été retrouvé par **bruteforce** avec Hashcat en mode JWT (`-m 16500`) et attaque par masque (`-a 3`) :

```bash
hashcat -m 16500 token.txt -a 3 -i '?a?a?a?a'
```

| Option | Description |
|--------|-------------|
| `-m 16500` | Mode JWT |
| `token.txt` | Fichier contenant le token |
| `-a 3` | Attaque par masque (brute-force) |
| `-i` | Mode incrémental (1 à N caractères) |
| `?a?a?a?a` | Tous les caractères ASCII imprimables, jusqu'à 4 chars |

---

### Q5 — Generate a new verified signature ticket with low privilege `(Format: String.String.String)`

**Réponse :**
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiQlRMe180X0V5ZXN9IiwiaWF0Ijo5MDAwMDAwMCwibmFtZSI6IkdyZWF0RXhwIiwiYWRtaW4iOmZhbHNlfQ.nMXNFvttCvtDcpswOQA8u_LpURwv6ZrCJ-ftIXegtX4
```

Avec le secret `bT!0` et [jwt.io](https://jwt.io), modification du payload :

```json
"admin": true  →  "admin": false
```

Le site recalcule automatiquement une signature valide avec le secret.

---

## 🛠️ Outils utilisés

| Outil | Usage |
|-------|-------|
| [CyberChef](https://gchq.github.io/CyberChef) | Décodage du token JWT |
| [jwt.io](https://jwt.io) | Analyse et forge du token |
| [Hashcat](https://hashcat.net) | Bruteforce du secret (`-m 16500`) |

---

## 📚 Ressources

- [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [jwt.io — Introduction](https://jwt.io/introduction)
- [Wikipedia — JWT (FR)](https://fr.wikipedia.org/wiki/JSON_Web_Token)
- [Hashcat Wiki — JWT mode](https://hashcat.net/wiki/doku.php?id=hashcat)
