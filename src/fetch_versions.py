import urllib.request
import re
import json
import time
import os

with open(os.path.join(os.path.dirname(__file__), "apps.json"), "r") as f:
    apps = json.load(f)["apps"]

# Régupère la version de l'application depuis l'App Store
# Retoune none en cas d'erreur ou si la version n'est pas trouvée
def get_appstore_version(app_store_id):
    try:
        url = f"https://itunes.apple.com/lookup?bundleId={app_store_id}"
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)
            if data.get('resultCount') == 1:
                v = data['results'][0]['version']
                return v
            else:
                return None
    except Exception:
        return None

# Régupère la version de l'application depuis le Play Store
# Retoune none en cas d'erreur ou si la version n'est pas trouvée
def get_playstore_version(play_store_id):
    try:
        with urllib.request.urlopen("https://play.google.com/store/apps/details?id="+play_store_id) as response:
            html = response.read().decode('utf-8')
            match = re.search(r'\[\[\[\"(\d+\.\d+\.\d+)', html)
            if match:
                return match.group(1)
            else:
                return None
    except Exception:
        return None

for app in apps:
    app_name = app["app_name"]
    app_store_id = app.get("app_store_id")
    appstore_version = get_appstore_version(app_store_id) if app_store_id else None
    play_store_id = app.get("play_store_id")
    playstore_version = get_playstore_version(play_store_id) if play_store_id else None
    # Récupère le timestamp actuel
    timestamp = int(time.time())

    # Préparation du contenu à écrire dans le fichier (json)
    content = {
        "app_name": app_name,
        "play_store_version": playstore_version,
        "app_store_version": appstore_version,
        "timestamp": timestamp
    }
    
    if content:
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(parent_dir, f"{app_name}.version")
        with open(file_path, "w") as f:
            f.write(json.dumps(content, ensure_ascii=False, indent=2))
    else:
        print(f"Version not found for {app_name}")
