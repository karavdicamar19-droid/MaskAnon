import os
import requests
import time
import sys

def animacija_naslova():
    os.system("clear")
    # Raw string da se izbjegne SyntaxWarning
    naslov = r"""
\033[1;31m  __  __               _                       
 |  \/  |             | |                      
 | \  / |  __ _  ___  | | __  __ _  _ __   ___  
 | |\/| | / _` |/ __| | |/ / / _` || '_ \ / _ \ 
 | |  | || (_| |\__ \ |   < | (_| || | | || (_) |
 |_|  |_| \__,_||___/ |_|\_\ \__,_||_| |_| \___/ \033[0m
    """
    print(naslov)
    print("\033[1;37m" + "="*55 + "\033[0m")

def potpis():
    print("\n\n\033[2m\033[3mCreated by: amar anon karavdic, paklenabasta.com\033[0m")

def main():
    animacija_naslova()
    
    # KORAK 1: TUNELI - JEDAN ISPOD DRUGOG
    print("\033[1;34m[ KORAK 1 ] Odaberi Tunel:\033[0m")
    print("\033[1;33m[1]\033[0m Ngrok (Pozadina - treba API)")
    print("\033[1;33m[2]\033[0m Cloudflare (Pozadina - Argo)")
    print("\033[1;33m[3]\033[0m Serveo (SSH - Manuelno)")
    print("\033[1;33m[4]\033[0m Localhost.run (SSH - Manuelno)")
    print("\033[1;33m[5]\033[0m Localtonet (Stabilna rezerva)")
    print("\033[1;33m[6]\033[0m Ručni unos linka (npr. paklenabasta.com)")
    
    t_izbor = input("\n\033[1;32m[?]\033[0m Tvoj izbor (1-6): ")
    
    url_napadaca = ""

    if t_izbor == "6":
        url_napadaca = input("[>] Unesi svoj URL: ")
    elif t_izbor == "1":
        api = input("[>] Ngrok Authtoken: ")
        os.system(f"ngrok config add-authtoken {api} > /dev/null 2>&1")
        os.system("pkill -f ngrok && nohup ngrok http 8080 > /dev/null 2>&1 &")
        print("[+] Palim Ngrok... (cekaj 8s)"); time.sleep(8)
        try:
            url_napadaca = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
        except: url_napadaca = None
    elif t_izbor == "2":
        os.system("pkill -f cloudflared && nohup cloudflared tunnel --url http://localhost:8080 > cf.log 2>&1 &")
        print("[+] Palim Cloudflare... (cekaj 8s)"); time.sleep(8)
        os.system("grep -o 'https://[-0-9a-z.]*trycloudflare.com' cf.log > link.txt")
        try:
            with open("link.txt", "r") as f: url_napadaca = f.read().strip()
        except: url_napadaca = None
    else:
        print("\033[1;31m[!] Pokreni tunel u drugom prozoru!\033[0m")
        url_napadaca = input("[>] Unesi link koji si dobio: ")

    if not url_napadaca:
        print("\033[1;31m[✘] Greška: Tunel nije startao!\033[0m"); return

    # KORAK 2: MASKE - JEDNA ISPOD DRUGE
    animacija_naslova()
    print(f"\033[1;32m[ TUNEL AKTIVAN ] {url_napadaca}\033[0m")
    print("\n\033[1;34m[ KORAK 2 ] Metode Maskiranja:\033[0m")
    print("\033[1;33m[1]\033[0m Maska BEZ @ (is.gd - najbolje)")
    print("\033[1;33m[2]\033[0m Maska BEZ @ (TinyURL - rezerva)")
    print("\033[1;33m[3]\033[0m Double Mask (TinyURL + is.gd)")
    print("\033[1;33m[4]\033[0m Social Preview (Facebook Meta)")
    print("\033[1;33m[5]\033[0m QR Kod Generator")
    print("\033[1;33m[6]\033[0m Custom Domain Link")
    
    m_izbor = input("\n\033[1;32m[?]\033[0m Tvoj izbor (1-6): ")
    maska_raw = input("\n[!] Naziv maske (npr. fb-prijava): ")
    oznaka = maska_raw.replace(".", "_").replace("-", "_")[:30]

    print("\n[+] Generišem finalni link...")
    rezultat = ""
    try:
        if m_izbor in ["1", "4", "5"]:
            rezultat = requests.get(f"https://is.gd/create.php?format=simple&url={url_napadaca}&shorturl={oznaka}").text
        elif m_izbor == "2":
            rezultat = requests.get(f"http://tinyurl.com/api-create.php?url={url_napadaca}").text
        elif m_izbor == "3":
            t = requests.get(f"http://tinyurl.com/api-create.php?url={url_napadaca}").text
            rezultat = requests.get(f"https://is.gd/create.php?format=simple&url={t}&shorturl={oznaka}").text
        elif m_izbor == "6":
            domena = input("[>] Unesi svoju domenu: ")
            rezultat = f"https://{domena}/{oznaka}"

        # FIX ZA BLACKLIST
        if "Error" in rezultat or "blacklist" in rezultat.lower():
            print("\033[1;31m[!] Detektovano! Automatski koristim TinyURL...\033[0m")
            rezultat = requests.get(f"http://tinyurl.com/api-create.php?url={url_napadaca}").text

        print("\n" + "X"*55)
        print(f" GOTOVO! TVOJ LINK: \033[1;32m{rezultat}\033[0m")
        print("X"*55)

        if m_izbor == "5":
            os.system(f"qrencode -t ANSI256 '{rezultat}'")

    except:
        print("[!] Greška u konekciji sa serverima.")

    potpis()

if __name__ == "__main__":
    main()
