import requests
from bs4 import BeautifulSoup

# 사용자 설정 정보
TOKEN = "8615185807:AAH12DVdri3rFtn0rxF6YsSqJqq-sA6Ro3M"
CHAT_ID = "8647440462"
URL = "https://m.pokemonstore.co.kr/pages/product/list.html?depth=2&categoryNo=488359"

def send_telegram(message):
    target_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    requests.get(target_url, params=params)

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        # 한글 깨짐 방지
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 포켓몬 스토어 상품 리스트 구역 찾기
        items = soup.select('.prd-item')
        
        if not items:
            print("상품 목록을 찾을 수 없습니다. 사이트 구조를 확인해보세요.")
            return

        for item in items:
            name_tag = item.select_one('.name')
            if not name_tag:
                continue
                
            name = name_tag.text.strip()
            # 전체 텍스트 중 '품절'이 포함되어 있는지 확인
            is_sold_out = "품절" in item.text 
            
            if not is_sold_out:
                # 품절이 아닌 상품 발견 시 알림 전송
                msg = f"🌟 [포켓몬 센터 로고핀] 재입고 알림! 🌟\n\n상품명: {name}\n지금 바로 확인하세요!\n{URL}"
                send_telegram(msg)
                print(f"알림 전송 완료: {name}")
                
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    check_stock()
