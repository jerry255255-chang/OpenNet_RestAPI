import pytest
from api_client import JsonPlaceholderClient, GeckoClient
import time

# 獲取文章
@pytest.mark.parametrize("post_id, expected_status", [
    (1, 200),    # API-01：存在的文章 
    (999, 404),  # API-02：不存在的文章 
], ids=["article exist", "article not exist"])
def test_get_post_status(post_id, expected_status):
    """
    步驟：呼叫 GET /posts/{id} 
    預期結果：回傳狀態碼應與預期相符
    驗證方式：使用 status_code 進行斷言 
    """
    client = JsonPlaceholderClient()
    response = client.get_post(post_id)
    assert response.status_code == expected_status

# 建立文章 (驗證資料完整性)
# API-03
def test_create_post_content():
    """
    步驟：發送 POST 請求建立新文章 
    預期結果：回傳 201 且包含我們發送的標題
    驗證方式：驗證 JSON 中的 title 欄位 
    """
    client = JsonPlaceholderClient()
    payload = {
        "title": "Gemini Test",
        "body": "This is a test post.",
        "userId": 1
    }
    response = client.create_post(payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data  # 驗證系統有產生新 ID

@pytest.mark.parametrize("vs_currency, expected_status, expect_price", [
    ("usd", 200, True),   # API-04：比特幣USD 價格與時間戳記驗證
    ("xyz", 200, False),  # API-05 :不存在的貨幣類型 (XYZ) 
], ids=["valid currency usd", "invalid currency xyz"])
def test_bitcoin_price_dynamic(vs_currency, expected_status, expect_price):
    client = GeckoClient()
    response = client.get_bitcoin_price(vs_currency)
    
    assert response.status_code == expected_status
    data = response.json()
    #print(data)  # testing purpose
    
    if expect_price:
        # 1. 驗證價格是否為大於 0 的浮點數 (動態數值驗證)
        price = data['bitcoin'][vs_currency]
        assert isinstance(price, (int, float))
        assert price > 0
        
        # 2. 驗證時間戳記是否在合理範圍內 (離現在不超過 5 分鐘)
        if 'last_updated_at' not in data['bitcoin']:
            pytest.fail("Missing last_updated_at field")
        updated_time = data['bitcoin']['last_updated_at']
        current_time = int(time.time())
        assert abs(current_time - updated_time) < 300 
    else:
        assert vs_currency not in data['bitcoin']