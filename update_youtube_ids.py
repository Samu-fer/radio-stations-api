import os
import json
import requests

API_KEY = os.environ.get("YOUTUBE_API_KEY")
JSON_PATH = "stations.json"

def get_active_live_id(channel_id):
    if not API_KEY:
        print("API Key no encontrada.")
        return None
    
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "eventType": "live",
        "type": "video",
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        items = data.get("items", [])
        if items:
            return items[0]["id"]["videoId"]
    except Exception as e:
        print(f"Error consultando la API para {channel_id}: {e}")
    
    return None

def main():
    if not os.path.exists(JSON_PATH):
        print(f"No se encontró el archivo {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        stations = json.load(f)

    updated = False
    for station in stations:
        channel_id = station.get("channelId")
        if channel_id:
            print(f"Buscando directo activo para: {station['name']}...")
            live_id = get_active_live_id(channel_id)
            if live_id:
                new_url = f"https://www.youtube.com/watch?v={live_id}"
                if station["streamUrl"] != new_url:
                    station["streamUrl"] = new_url
                    updated = True
                    print(f" -> Actualizado a: {new_url}")
            else:
                print(" -> No está transmitiendo en vivo actualmente.")

    if updated:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(stations, f, indent=4, ensure_ascii=False)
        print("Archivo stations.json actualizado exitosamente.")
    else:
        print("No hubo cambios en las transmisiones.")

if __name__ == "__main__":
    main()
