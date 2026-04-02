import requests
from bs4 import BeautifulSoup

# 님의 정보 (이미 확인된 값)
TOKEN = "8615185807:AAH12DVdri3rFtn0rxF6YsSqJqq-sA6Ro3M"
CHAT_ID = "8647440462"
URL = "https://m.pokemonstore.co.kr/pages/product/list.html?depth=2&categoryNo=488359"

def check_stock():
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('.prd-item')
        
        for item in items:
            name = item.select_one('.name').text.strip()
            # '품절' 마크가 없는 카드가 있는지 확인
            if "품절" not in item.text:
                msg = f"🃏 [포켓몬 카드 재입고!] 🃏\n\n상품명: {name}\n지금 바로 확인하세요!\n{URL}"
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    check_stock()
