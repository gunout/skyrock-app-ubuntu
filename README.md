<div align="center">

# 📻 Skyrock Radio

### Lecteur radio minimaliste pour **Skyrock** et ses webradios

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5%2B-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PyQt6/)
[![mpv](https://img.shields.io/badge/mpv-player-691F69?style=for-the-badge&logo=mpv&logoColor=white)](https://mpv.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%2B-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](#)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-0078D6?style=for-the-badge&logo=linux&logoColor=white)](#)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen?style=for-the-badge)](#)
[![PRs](https://img.shields.io/badge/PRs-Welcome-ff69b4?style=for-the-badge)](https://github.com/gunout/skyrock-app-ubuntu/pulls)
[![Made with ❤️](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red?style=for-the-badge)](#)

<br>

<img src="https://img.shields.io/badge/Skyrock-FF0000?style=flat-square" />
<img src="https://img.shields.io/badge/Rap%20%26%20RnB-FF3B3B?style=flat-square" />
<img src="https://img.shields.io/badge/100%25%20Fran%C3%A7ais-FF9E00?style=flat-square" />
<img src="https://img.shields.io/badge/Klassiks-FFD700?style=flat-square" />
<img src="https://img.shields.io/badge/Urban-9B59B6?style=flat-square" />
<img src="https://img.shields.io/badge/Hit%20US-3498DB?style=flat-square" />
<img src="https://img.shields.io/badge/PLM-2ECC71?style=flat-square" />
<img src="https://img.shields.io/badge/Abidjan-E67E22?style=flat-square" />

</div>

---

## ✨ Aperçu

**Skyrock Radio** est un lecteur radio **ultra-léger**, **frameless** et **moderne** qui regroupe les principales webradios du réseau **Skyrock**.

Interface sombre, visualiseur audio animé, contrôles repliables, popup de liens vers les sections du site officiel : tout est pensé pour une expérience fluide et discrète.

---

## 🎯 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🎧 **8 webradios Skyrock** | Skyrock, Rap & RnB, 100% Français, Klassiks, Urban, Hit US, PLM, Abidjan |
| 🎨 **Interface frameless** | Design sombre, coins arrondis, drag & resize natifs |
| 📊 **Visualiseur audio** | 32 barres animées en temps réel |
| 🔇 **Contrôles complets** | Play / Pause / Stop / Mute / Volume |
| 🪗 **Repli automatique** | Les contrôles se cachent après 3,5 s d'inactivité |
| 🔽 **Fenêtre repliable** | Mode mini pour ne garder que la barre de titre |
| 🌐 **Popup sites** | Accès direct aux sections de skyrock.fm |
| ⚡ **Léger** | Basé sur `mpv` — consommation minimale |

---

## 🚀 Installation rapide

### Méthode automatique (recommandée)

```bash
git clone https://github.com/gunout/skyrock-app-ubuntu.git
cd skyrock-app-ubuntu
chmod +x install.sh
./install.sh
```

Le script détecte ton OS, installe `mpv`, `ffmpeg`, crée un environnement virtuel, installe les dépendances Python et génère un lanceur `run.sh`.

### Lancement

```bash
./run.sh
```

---

## 🛠️ Installation manuelle

<details>
<summary><b>Clique pour déplier</b></summary>

### 1. Prérequis système

**Debian / Ubuntu**
```bash
sudo apt update
sudo apt install -y mpv ffmpeg python3-pip python3-venv \
                    libxcb-cursor0 libxkbcommon-x11-0
```

**Fedora / RHEL**
```bash
sudo dnf install -y mpv ffmpeg python3-pip python3-virtualenv
```

**Arch Linux**
```bash
sudo pacman -S mpv ffmpeg python-pip python-virtualenv
```

**macOS (Homebrew)**
```bash
brew install mpv ffmpeg python@3.11
```

### 2. Environnement Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Lancement

```bash
python3 skyrock_radio.py
```

</details>

---

## 📁 Structure du projet

```
skyrock-app-ubuntu/
├── skyrock_radio.py    # Application principale
├── install.sh          # Script d'installation automatique
├── run.sh              # Lanceur généré (après install)
├── requirements.txt    # Dépendances Python
├── logo.png            # Logo affiché dans le HUD (optionnel)
├── README.md
└── LICENSE
```

---

## 📦 Dépendances

| Paquet | Version | Rôle |
|---|---|---|
| `PyQt6` | ≥ 6.5.0 | Interface graphique |
| `python-mpv` | ≥ 1.0.4 | Lecture audio |
| `mpv` (système) | ≥ 0.35 | Backend audio |
| `ffmpeg` (système) | ≥ 5.0 | Décodage des flux |

---

## ⌨️ Raccourcis & interactions

| Action | Geste |
|---|---|
| Déplacer la fenêtre | Glisser la souris sur la barre du haut |
| Redimensionner | Glisser les bords / coins |
| Lire une station | **Double-clic** sur la station |
| Replier les contrôles | Bouton `⌄` en bas à droite |
| Replier la fenêtre | Bouton `⌃` en haut à droite |
| Ouvrir le popup sites | Bouton `SITES` |

---

## 🌍 Webradios incluses

| Webradio | Flux |
|---|---|
| 🔴 **Skyrock** | `https://icecast.skyrock.net/s/natio_aac_128k` |
| 🎤 **Rap & RnB Non-Stop** | `https://icecast.skyrock.net/s/rap_rnb_aac_128k` |
| 🇫🇷 **100% Français** | `https://icecast.skyrock.net/s/francais_aac_128k` |
| 💿 **Klassiks** | `https://icecast.skyrock.net/s/klassiks_aac_128k` |
| 🏙️ **Urban Music** | `https://icecast.skyrock.net/s/urban_music_aac_128k` |
| 🇺🇸 **Hit US** | `https://icecast.skyrock.net/s/hit_us_aac_128k` |
| 🎖️ **PLM** | `https://icecast.skyrock.net/s/plm_aac_128k` |
| 🌍 **Abidjan** | `https://icecast.skyrock.net/s/abidjan_aac_64k` |

> 💡 **Astuce** : Si un flux ne fonctionne pas, ouvre [skyrock.fm/radios](https://skyrock.fm/radios), appuie sur `F12` → onglet **Network** → filtre **Media**, puis lance la lecture pour récupérer l'URL exacte.

---

## 🤝 Contribuer

Les contributions sont **les bienvenues** !

1. Fork le projet
2. Crée une branche (`git checkout -b feature/ma-feature`)
3. Commit (`git commit -m 'Ajout de ma feature'`)
4. Push (`git push origin feature/ma-feature`)
5. Ouvre une **Pull Request**

---

## 🐛 Signaler un bug

Ouvre une [issue](https://github.com/gunout/skyrock-app-ubuntu/issues) avec :
- Ton OS et version
- La version Python
- Les logs d'erreur

---

## 📜 Licence

Distribué sous licence **MIT**. Voir [`LICENSE`](https://github.com/gunout/skyrock-app-ubuntu/blob/main/LICENSE) pour plus d'infos.

---

## 🙏 Remerciements

- [Skyrock](https://skyrock.fm/) pour les flux radio
- [mpv](https://mpv.io/) pour le backend audio
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) pour l'interface

---

<div align="center">

**Fait avec ❤️ par [gunout](https://github.com/gunout)**

⭐ N'oublie pas de mettre une étoile si ce projet t'a plu !

</div>
