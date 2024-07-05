import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Danh sách các URL cần lấy dữ liệu
urls = [
    'https://giavang.org/trong-nuoc/pnj/lich-su/2015-01-01.html'
 
]

# Đường dẫn tới tệp CSV hiện có
csv_file_path = 'path_to_your_existing_file.csv'

# Đọc tệp CSV hiện có (nếu tồn tại)
try:
    existing_df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    existing_df = pd.DataFrame(columns=['date', 'buy_price', 'sell_price'])

# Hàm để lấy dữ liệu từ URL
def get_gold_prices(url):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tìm phần tử có lớp 'gold-price-box'
    gold_price_box = soup.find('div', class_='gold-price-box')
    
    # Tìm giá 'Mua vào'
    buy_price_element = gold_price_box.find('div', class_='box-cgre').find('span', class_='gold-price')
    print(buy_price_element.text)
    buy_price = buy_price_element.text.strip().replace(".",'')[:-13]
    print(buy_price)
    
    
    # Tìm giá 'Bán ra'
    sell_price_element = gold_price_box.find('div', class_='box-cred').find('span', class_='gold-price')
    sell_price = sell_price_element.text.strip().replace(".",'')[:-13]
    
    # Lấy ngày từ URL
    date_str = url.split('/')[-1].split('.')[0]
    
    return date_str, buy_price, sell_price

# Lặp qua các URL và lấy dữ liệu
for url in urls:
    date, buy_price, sell_price = get_gold_prices(url)
    
    # Tạo DataFrame với dữ liệu mới
    new_data = {
        'date': [date],
        'buy_price': [buy_price],
        'sell_price': [sell_price]
    }
    new_df = pd.DataFrame(new_data)
    
    # Thêm dữ liệu mới vào DataFrame hiện có
    existing_df = pd.concat([existing_df, new_df], ignore_index=True)

# Ghi DataFrame trở lại tệp CSV
existing_df.to_csv(csv_file_path, index=False)

# In DataFrame để kiểm tra
print(existing_df)
