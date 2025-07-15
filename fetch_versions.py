import urllib.request
import re
import json

with open("apps.json", "r") as f:
  apps = json.load(f)["apps"]

# Régupère la version de l'application depuis le Play Store
def get_playstore_version(play_store_id):
    with urllib.request.urlopen("https://play.google.com/store/apps/details?id="+play_store_id) as response:
        html = response.read().decode('utf-8')
        match = re.search(r'\[\[\[\"(\d+\.\d+\.\d+)', html)
        if match:
            return match.group(1)
        else:
            return None

# Régupère la version de l'application depuis l'App Store
def get_appstore_version(app_store_id):
    url = f"https://itunes.apple.com/lookup?bundleId={app_store_id}"
    with urllib.request.urlopen(url) as response:
        body = response.read().decode('utf-8')
        data = json.loads(body)
        if data.get('resultCount') == 1:
            v = data['results'][0]['version']
            return v
        else:
            return None

for app in apps:
    app_name = app["app_name"]
    playstore_package_name = app["play_store_id"]
    appstore_package_name = app["app_store_id"]
    playstore_version = get_playstore_version(playstore_package_name)
    appstore_version = get_appstore_version(appstore_package_name)

    # Préparation du contenu à écrire dans le fichier (json)
    content = {
        "app_name": app_name,
        "play_store_version": playstore_version,
        "app_store_version": appstore_version
    }
    
    if content:
        with open(f"{app_name}.version", "w") as f:
            f.write(json.dumps(content, ensure_ascii=False, indent=2))
    else:
        print(f"Version not found for {app_name}")
