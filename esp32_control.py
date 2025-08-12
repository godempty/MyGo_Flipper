import requests

ESP_IP = "192.168.50.214"
ESP_PORT = 80
ESP_API_URL = f"http://{ESP_IP}:{ESP_PORT}"
ESP_API_POSITION = "/spin"
ESP_API_STEP = "/step"


def control_esp(value):
    try:
        data = {"position": value}
        response = requests.post(f"{ESP_API_URL}{ESP_API_POSITION}", timeout=5, json=data)
        return response.json()
    except Exception as e:
        return {"error" : e}


def stepping(value):
    data = {"step": value}
    response = requests.post(f"{ESP_API_URL}{ESP_API_STEP}", json=data)
    return response.json()
