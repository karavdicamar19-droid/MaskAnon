# 👺 MaskAnon

**The Ultimate URL Masking & Tunneling Tool for Termux / Linux**

MaskAnon je moćna Python skripta dizajnirana za automatizaciju procesa podizanja lokalnih tunela (Ngrok, Cloudflare) i njihovog maskiranja u URL-ove koji izgledaju legitimno (bez `@` simbola) koristeći razne servise za skraćivanje i QR kodove.

![MaskAnon Screenshot](https://raw.githubusercontent.com/TvojGitHubUsername/MaskAnon/main/screenshot.png) *(Ovdje kasnije možeš ubaciti link svoje slike ako je dodaš na GitHub)*

## 🚀 Mogućnosti (Features)
* **Auto-Tunneling:** Automatski pokreće Ngrok ili Cloudflare u pozadini i vadi aktivni link.
* **Multi-Tunnel Podrška:** Podržava Ngrok, Cloudflare Argo, Serveo i Localhost.run.
* **Stealth Maskiranje:** Sakriva ružne tunel linkove iza `is.gd` ili `tinyurl` servisa (npr. `is.gd/tvoja_maska`).
* **Double Masking:** Korištenje dva servisa odjednom za maksimalno izbjegavanje filtera.
* **QR Kod Generator:** Automatski generiše ANSI QR kod direktno u tvom terminalu.
* **Anti-Blacklist Sistem:** Ako jedan servis blokira tvoj naziv, skripta automatski prebacuje na rezervni.

## ⚙️ Instalacija (Termux / Kali Linux)

Otvori terminal i ukucaj sljedeće komande:

```bash
git clone [https://github.com/TvojGitHubUsername/MaskAnon.git](https://github.com/TvojGitHubUsername/MaskAnon.git)
cd MaskAnon
chmod +x setup.sh
./setup.sh

#!/bin/bash
# MaskAnon Automatska Instalacija Termux

echo -e "\e[1;31m Instaliram zavisnosti za MaskAnon...\e[0m"
sleep 2

pkg update && pkg upgrade -y
pkg install python git qrencode wget curl openssh -y
pip install requests

echo -e "\e[1;32m[✔] Instalacija završena! Pokreni sa: python mask.py\e[0m"

#Linux,Ubuntu...
git clone url && sudo apt install ngrok && cd fajl && python mask.py

#Upozorenje
Ne koristi za zloupotrebu, ovo je za Eticke Hakere.
#Vlasnik
Amar Anon Karavdic, Paklenabasta.com, hackaton.
