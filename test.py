import requests
import os

def download_image(url, file_name):
    """Downloads an image from a URL and saves it to a file."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name}. Status code: {response.status_code}")

def get_steamdb_images(app_id):
    """Fetches and downloads images for a given Steam app ID from SteamDB."""
    base_url = f"https://steamcdn-a.akamaihd.net/steam/apps/{app_id}/"
    images = {
        "header": f"{base_url}header.jpg",
        "library_hero": f"{base_url}library_hero.jpg",
        "library_capsule": f"{base_url}library_capsule.jpg",
        "library_600x900": f"{base_url}library_600x900.jpg",
        "library_hero_2x": f"{base_url}library_hero_2x.jpg"
    }

    for image_type, url in images.items():
        file_name = f"{app_id}_{image_type}.jpg"
        download_image(url, file_name)

if __name__ == "__main__":
    # Replace 'APP_ID' with the actual Steam App ID of the game you want to download assets for
    app_id = "105600"
    get_steamdb_images(app_id)