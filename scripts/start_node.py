from comcoin import node

if __name__ == "__main__":
    print("🚀 Starting ComCoin node on http://localhost:5000")
    node.app.run(host='0.0.0.0', port=5000)
