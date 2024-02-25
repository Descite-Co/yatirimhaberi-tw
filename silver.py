import requests

def get_data(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code)
        return None

json_data = get_data('https://api.genelpara.com/embed/para-birimleri.json')

if json_data:
    data = json_data.get('GAG')
    if data:
        print('#Gümüş:')
        print(f'Fiyat: ₺{data["satis"]}')
        print(f'Değişim: {data["degisim"]}%\n')
    else:
        print('Gümüş verisi bulunamadı.')
