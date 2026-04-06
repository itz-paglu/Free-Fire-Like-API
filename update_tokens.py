import requests
import json

UIDPASS_FILE = "uidpass.json"
TOKEN_FILE = "tokens.json"
API_URL = "http://127.0.0.1:8010/token"

def read_uidpass():
    with open(UIDPASS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_token(uid, password):
    url = f"{API_URL}?uid={uid}&password={password}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("token")
    except Exception as e:
        print(f"Error fetching token for UID {uid}: {e}")
        return None

def update_token_file(token_list):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_list, f, ensure_ascii=False, indent=4)

def main():
    uidpass_list = read_uidpass()
    new_tokens = []
    for item in uidpass_list:
        token = fetch_token(item["uid"], item["password"])
        if token:
            new_tokens.append({"token": token})
    if new_tokens:
        update_token_file(new_tokens)
        print("tokens.json updated successfully.")
    else:
        print("No tokens updated.")

if __name__ == "__main__":
    main()
