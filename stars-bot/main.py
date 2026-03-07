from flask import Flask, request, jsonify
from flask_cors import CORS  # для разрешения запросов с вашего домена
from fragment_api_lib.client import FragmentAPIClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # разрешить кросс-доменные запросы (если фронтенд и бэкенд на разных портах)

client = FragmentAPIClient()
SEED = os.getenv("TON_WALLET_SEED")

if not SEED:
    raise ValueError("Seed не найден! Проверьте .env файл.")

@app.route('/api/buy-stars', methods=['POST'])
def buy_stars():
    data = request.json
    username = data.get('username')
    amount = data.get('amount')

    if not username or not amount:
        return jsonify({"success": False, "error": "Missing username or amount"}), 400

    try:
        # Убираем @ если есть
        clean_username = username.lstrip('@')
        result = client.buy_stars_without_kyc(
            username=clean_username,
            amount=int(amount),
            seed=SEED
        )
        # result содержит данные об успешной покупке
        return jsonify({"success": True, "data": result})
    except Exception as e:
        app.logger.error(f"Purchase error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)