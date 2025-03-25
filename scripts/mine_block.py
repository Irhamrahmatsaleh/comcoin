import requests

def main():
    print("🔨 ComCoin Miner CLI")
    miner_address = input("🏦 Enter your public key (wallet address): ").strip()

    response = requests.post("http://localhost:5000/mine", json={
        "miner_address": miner_address
    })

    if response.status_code == 200:
        print(f"✅ Success: {response.text}")
    else:
        print(f"❌ Failed: {response.text}")

if __name__ == "__main__":
    main()
