<div align="center">
  <img src="https://via.placeholder.com/800x400.png?text=MASKANON+v6.0" alt="MaskAnon Banner">
</div>

# 👺 MASKANON
**The Ultimate URL Masking & Tunneling Tool for Termux / Linux**

**MaskAnon** je moćna, automatizovana Python skripta dizajnirana za "sakrivanje" dugačkih i sumnjivih linkova (poput onih koje generišu lokalni serveri). Alat automatski podiže tunele u pozadini, hvata generisani URL i provlači ga kroz napredne filtere za maskiranje, stvarajući linkove koji izgledaju potpuno bezopasno (npr. `is.gd/facebook_prijava_sigurnost`).

Ovo je savršen alat za testiranje sigurnosti (penetration testing), simulacije socijalnog inženjeringa i izbjegavanje anti-spam filtera na platformama za komunikaciju.

---

## 🌐 Kako funkcionišu Tuneli u MaskAnonu?
Da bi neko preko interneta pristupio tvom lokalnom fajlu ili lažnoj stranici na tvom telefonu/kompjuteru, potreban ti je **Tunel**. MaskAnon nudi nekoliko opcija:

* **[1] Ngrok (Pozadina - treba API):** Najstabilniji servis. **Zahtijeva API Authtoken** (registruj se besplatno na ngrok.com). MaskAnon automatski sprema tvoj ključ i sam "krade" link.
* **[2] Cloudflare (Pozadina - Argo):** Vrhunska alternativa. **Ne traži registraciju ni API ključ.** Skripta ga pokreće u pozadini i automatski "čupa" `trycloudflare.com` link iz logova.
* **[3] & [4] SSH Tuneli (Serveo & Localhost.run):** Ne zahtijevaju dodatnu instalaciju. Pokreću se ručno u drugom prozoru terminala.

---

## ⚙️ Instalacija (Termux / Kali Linux)

Otvori terminal i ukucaj sljedeće komande redom kako bi instalirao alat i sve potrebne pakete:

```bash
# 1. Ažuriranje sistema i instalacija paketa
pkg update && pkg upgrade -y
pkg install python git qrencode wget curl openssh -y
pip install requests

# 2. Preuzimanje alata sa GitHuba
git clone [https://github.com/TvojGitHubUsername/MaskAnon.git](https://github.com/TvojGitHubUsername/MaskAnon.git)
cd MaskAnon

# 3. Pokretanje alata
python mask.py
