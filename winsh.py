import sys
import os
import json
import datetime
import requests
import ctypes
from winsh_tui import WinShieldTUI

WINSH_VERSION = "v1.4.2-Stable"
CONFIG_FILE = "winshield_config.json"
WATCHED_DIR = r"C:\WinShieldProtected"
LOG_FILE = "winshield_history.log"
SERVER_URL = "127.0.0" # Hier Server-IP eintragen

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {WATCHED_DIR: []}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def handle_connection_error():
    print("\n" + "="*70)
    print(f"🚨 Fehler 289: Verbindungsfehler.")
    print("   Zentraler Server konnte nicht erreicht werden.")
    print(f"   Ihre momentane Version von WinShield: [{WINSH_VERSION}]")
    print("="*70 + "\n")

def show_24h_report():
    print("\n📊 WinShield - Sicherheitsbericht (Letzte 24 Stunden)")
    print("====================================================")
    if not os.path.exists(LOG_FILE):
        print("    Keine Logdaten vorhanden.")
        return
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(days=1)
    block_count = 0
    with open(LOG_FILE, "r") as f:
        for line in f:
            if not line.startswith("["): continue
            try:
                time_str = line.split("]")[0].replace("[", "")
                log_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                if log_time > one_day_ago and "[BLOCK]" in line:
                    block_count += 1
                    print(f" 🚨 {line.strip()}")
            except ValueError:
                continue
    print(f"\n📈 Abgewehrte Angriffe (Nö!): {block_count}\n")

def list_server_profiles():
    try:
        response = requests.get(f"{SERVER_URL}/profiles", timeout=4)
        if response.status_code == 200:
            print("\n🌐 Verfügbare globale WinShield-Profile:")
            print("=========================================")
            for pkg, desc in response.json().items():
                print(f"  • {pkg.ljust(25)} -> {desc}")
            print("\nInstallation über: manage WINSH update <profilname>\n")
        else:
            handle_connection_error()
    except:
        handle_connection_error()

def fetch_and_apply_profile(package_name):
    try:
        response = requests.get(f"{SERVER_URL}/profiles/{package_name}", timeout=4)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                config = load_config()
                added_count = 0
                for app in data["apps"]:
                    if app not in config[WATCHED_DIR]:
                        config[WATCHED_DIR].append(app)
                        added_count += 1
                save_config(config)
                print(f"[+] Erfolg! {added_count} Anwendung(en) für '{package_name}' importiert.")
        else:
            handle_connection_error()
    except:
        handle_connection_error()

def main():
    if not is_admin():
        print("[-] Fehler: Administratorrechte zwingend erforderlich!")
        sys.exit(1)

    if len(sys.argv) < 2 or sys.argv[1].upper() != "WINSH":
        print("\n🛡️  WinShield - Verwendung: manage WINSH [befehl]\n")
        sys.exit(1)

    if len(sys.argv) == 2:
        print("[*] Starte WinShield Terminal User Interface...")
        app = WinShieldTUI()
        app.run()
        sys.exit(0)

    command = sys.argv[2].lower()

    if command == "report":
        show_24h_report()
    elif command == "update":
        if len(sys.argv) < 4:
            list_server_profiles()
        else:
            fetch_and_apply_profile(sys.argv[3].lower())
    elif command == "allow":
        if len(sys.argv) < 4: return
        app_name = sys.argv[3].lower()
        config = load_config()
        if app_name not in config[WATCHED_DIR]:
            config[WATCHED_DIR].append(app_name)
            save_config(config)
            print(f"[+] '{app_name}' erlaubt.")
    elif command == "block":
        if len(sys.argv) < 4: return
        app_name = sys.argv[3].lower()
        config = load_config()
        if app_name in config[WATCHED_DIR]:
            config[WATCHED_DIR].remove(app_name)
            save_config(config)
            print(f"[-] '{app_name}' blockiert. Nö!")

if __name__ == "__main__":
    main()
