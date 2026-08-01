# 🔐 BTLO — Shiba Insider | Writeup

## 📋 Scenario

> Can you uncover the insider?

**Fichiers fournis :**
```
Insider.zip/
├── insider.pcap
└── file.zip/
    ├── README.txt
    └── ssdog1.jpeg
```

---

## 🧠 Méthodologie

### Approche générale

> Analyse d'une capture réseau (PCAP) pour extraire des credentials, puis investigation forensic sur une image via métadonnées et stéganographie.

---

## ❓ Questions & Réponses

### Q1 — What is the response message obtained from the PCAP file? `(Format: String)`

**Réponse : `use your own password`**

> Ouverture du fichier `insider.pcap` dans **Wireshark**, puis `Follow > TCP Stream`.  
> Le message était visible directement dans le stream.

---

### Q2 — What is the password of the ZIP file? `(Format: String)`

**Réponse : `redforever`**

Dans le stream TCP de la capture réseau :

```
Authorization: Basic ZmFrZWJsdWU6cmVkZm9yZXZlcg==
```

Reconnaissance du **Base64**, décodage avec la commande :

```bash
echo "ZmFrZWJsdWU6cmVkZm9yZXZlcg==" | base64 -d
```

| Option | Description |
|--------|-------------|
| `echo` | Affiche la chaîne encodée |
| `base64 -d` | Décode la chaîne Base64 |

> Résultat : `fakebluue:redforever` — le mot de passe est la partie après les `:`

---

### Q3 — Will more passwords be required? `(Format: Yes/No)`

**Réponse : `No`**

> Contenu du `README.txt` extrait du `file.zip` :  
> *"Shiba Dog has everything you need and decided that no more passwords will be needed"*

---

### Q4 — What is the name of a widely-used tool that can be used to obtain file information? `(Format: Tool)`

**Réponse : `exiftool`**

> Outil standard pour lire les métadonnées de fichiers (images, vidéos, documents).  
> Source : [exiftool.org](https://exiftool.org/)

---

### Q5 — What is the name and value of the interesting information obtained from the image file metadata? `(Format: Name:Value)`

**Réponse : `Technique:Steganography`**

Extraction des métadonnées de l'image :

```bash
exiftool ssdog1.jpeg
```

| Option | Description |
|--------|-------------|
| `exiftool` | Lit les métadonnées du fichier |
| `ssdog1.jpeg` | Fichier image cible |

> Le champ `Technique: Steganography` était visible directement dans le résultat.

---

### Q6 — Based on the answer from the previous question, what tool needs to be used to retrieve the information hidden in the file? `(Format: Tool)`

**Réponse : `steghide`**

> Juste en dessous du champ précédent dans les métadonnées :  
> `Technique Command : steghide`  
> Source : [steghide.com](https://steghide.com/)

---

### Q7 — Enter the ID retrieved. `(Format: ID)`

**Réponse : `0726ba878ea47de571777a`**

Extraction des données cachées dans l'image :

```bash
steghide extract -sf ssdog1.jpeg
```

| Option | Description |
|--------|-------------|
| `extract` | Mode extraction |
| `-sf` | Spécifie le fichier stégo source |
| `ssdog1.jpeg` | Fichier image contenant les données cachées |

---

## 🛠️ Outils utilisés

| Outil | Usage |
|-------|-------|
| [Wireshark](https://www.wireshark.org) | Analyse de la capture réseau PCAP |
| `base64` | Décodage des credentials encodés |
| [exiftool](https://exiftool.org) | Lecture des métadonnées de l'image |
| [steghide](https://steghide.com) | Extraction des données stéganographiées |

---

## 📚 Ressources

- [exiftool.org](https://exiftool.org/)
- [steghide.com](https://steghide.com/)
- [Commandes Linux](https://blog.stephane-robert.info/docs/admin-serveurs/linux/commandes/)
