import requests

class JsonPlaceholderClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_post(self, post_id):
        """獲取特定文章內容"""
        return requests.get(f"{self.BASE_URL}/posts/{post_id}")

    def create_post(self, data):
        """建立新文章"""
        return requests.post(f"{self.BASE_URL}/posts", json=data)
    
class GeckoClient:
    # CoinGecko 用於動態數據與時間戳記測試
    GECKO_BASE = "https://api.coingecko.com/api/v3"

    def get_bitcoin_price(self, vs_currencies="usd"):
        """
        獲取比特幣價格與最後更新時間
        回傳包含 vs_currencies 價格與 last_updated_at (Unix Timestamp)
        """
        params = {
            "ids": "bitcoin",
            "vs_currencies": vs_currencies,
            "include_last_updated_at": "true"
        }
        return requests.get(f"{self.GECKO_BASE}/simple/price", params=params)