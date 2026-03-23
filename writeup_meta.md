# 🔍 BTLO — META | OSINT/Forensics Challenge Writeup

## 📋 Scenario

> The attached images were posted by a criminal on the run, with the caption *"I'm roaming free. You will never catch me"*. We believe you can assist us in proving him wrong.

**Fichiers fournis :**
```
cf7becafebbb525b3c1df03785a2b9ee6b96e41c.zip
├── uploaded_1.JPG
└── uploaded_2.png
```

---

## 🧠 Méthodologie

### Qu'est-ce que les métadonnées EXIF ?

> EXIF (Exchangeable Image File Format) est un standard qui définit les informations stockées dans les fichiers image produits par les appareils photo numériques. Ces métadonnées peuvent contenir : le modèle de l'appareil, la date de prise de vue, les coordonnées GPS, les paramètres d'exposition, et des champs commentaires libres.

**Pourquoi c'est intéressant en forensics ?**

Les métadonnées EXIF sont souvent oubliées par les criminels lorsqu'ils publient des photos. Elles peuvent révéler des informations critiques sans que l'image elle-même ne les trahisse visuellement.

> ⚠️ Comme le suggère le commentaire trouvé dans ce challenge, les métadonnées peuvent être **altérées** volontairement — il faut donc toujours croiser plusieurs sources d'information.

---

## ❓ Questions & Réponses

### Q1 — What is the camera model? `(Format: String)`

**Réponse : `Canon EOS 550D`**

Extraction des métadonnées avec **ExifTool** :

```bash
exiftool uploaded_1.JPG
```

Recherche du champ pertinent dans la sortie (copie dans un fichier txt + `Ctrl+F` sur "model") :

```
Camera Model Name     : Canon EOS 550D
```

---

### Q2 — When was the picture taken? `(Format: YYYY:MM:DD HH:MM:SS)`

**Réponse : `2021:11:02 13:20:23`**

Même commande ExifTool, recherche du champ `Date/Time Original` :

```
Date/Time Original    : 2021:11:02 13:20:23
```

> ⚠️ Il existe plusieurs champs de date dans EXIF (`Create Date`, `Modify Date`, `Date/Time Original`). En forensics, **Date/Time Original** est le plus fiable — c'est la date capturée par le capteur au moment du déclenchement.

---

### Q3 — What does the comment on the first image say? `(Format: String)`

**Réponse : `relying on altered metadata to catch me?`**

Toujours via ExifTool, recherche du champ `Comment` dans les résultats :

```
Comment               : relying on altered metadata to catch me?
```

> 🧠 Ce commentaire est un indice du challenge : le criminel suggère que ses métadonnées ont été **falsifiées**. Cela justifie l'utilisation d'une **seconde méthode** (recherche inversée d'image) pour la question suivante, plutôt que de se fier aux coordonnées GPS potentiellement présentes.

---

### Q4 — Where could the criminal be? `(Format: City)`

**Réponse : `Kathmandu`**

Les métadonnées étant potentiellement altérées (cf. Q3), la localisation a été retrouvée par **recherche inversée d'image** :

**Outil utilisé :** [TinEye](https://tineye.com/)

```
Image soumise : uploaded_2.png
URL des résultats : https://tineye.com/search/04910167846981c6f62999acdf538d52de00d960?tags=&sort=score&order=desc&page=1
```

TinEye retrouve des occurrences de l'image sur le web, permettant d'identifier le lieu représenté : **Kathmandu, Népal**.

---

## 🛠️ Outils utilisés

| Outil | Usage |
|-------|-------|
| [ExifTool](https://exiftool.org) | Extraction des métadonnées EXIF |
| [TinEye](https://tineye.com) | Recherche inversée d'image (géolocalisation) |

---

## 📚 Ressources

- [ExifTool — Documentation officielle](https://exiftool.org/examples.html)
- [TinEye — Reverse Image Search](https://tineye.com/)
