import requests
from bs4 import BeautifulSoup
import yaml

with open("apps.yaml", "r") as f:
    apps = yaml.safe_load(f)["apps"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_playstore_version(package_name):
    url = f"https://play.google.com/store/apps/details?id={package_name}&hl=fr&gl=US"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    version = None
    for div in soup.find_all("div", class_="W4P4ne"):
        if "Version actuelle" in div.text or "Current Version" in div.text:
            version = div.find_next_sibling().text.strip()
            break
    return version

for app in apps:
    app_name = app["app_name"]
    package_name = app["package_name"]
    version = get_playstore_version(package_name)
    if version:
        with open(f"{app_name}.version", "w") as f:
            f.write(version)
    else:
        print(f"Version not found for {app_name}")
