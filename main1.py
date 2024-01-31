import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
def scrape_forex_rate(date, currency_code):
    # 设置Chrome浏览器路径
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    # 创建ChromeOptions对象
    chrome_options = Options()
    chrome_options.binary_location = chrome_path

    # 初始化浏览器
    browser = webdriver.Chrome(options=chrome_options)
    
    try:
        # 打开中国银行外汇牌价网站
        browser.get('https://www.boc.cn/sourcedb/whpj/')

        # 等待日期输入框可见并清空
        start_date_input = WebDriverWait(browser, 1000).until(
            EC.visibility_of_element_located((By.NAME, 'erectDate'))
        )
        start_date_input.clear()
        start_date_input.send_keys(date)

        # 等待结束日期输入框可见并清空
        end_date_input = WebDriverWait(browser, 1000).until(
            EC.visibility_of_element_located((By.NAME, 'nothing'))
        )
        end_date_input.clear()
        end_date_input.send_keys(date)

        # 使用Select类定位并选择货币
        currency_select = Select(browser.find_element(By.NAME, 'pjname'))

        # 等待货币选择框可见
        WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.NAME, 'pjname'))
        )

        currency_select.select_by_visible_text("美元")

        
        query_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@onclick="executeSearch()"]'))
        )
        query_button.click()

        # 等待加载完成
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//td[@align="left"][4]'))
        )

        # 获取现汇卖出价（取第一行数据）
        forex_rate = browser.find_element(By.XPATH, '//tr[@class="odd"]/td[4]').text

        # 打印到控制台
        print(f'{forex_rate}\n')

        # 将结果写入result.txt文件
        with open('result.txt', 'a',encoding='utf-8') as result_file:
            result_file.write(f'{date} {currency_code} 现汇卖出价: {forex_rate}\n')

    except Exception as e:
        print(f'发生异常: {e}')

    finally:
        # 关闭浏览器
        browser.quit()


if __name__ == '__main__':
    date_input = ""
    currency_code_input = ""
    
    if len(sys.argv) != 3:
        print('Usage: python3 yourcode.py <date> <currency_code>')
    else:
        date_input = sys.argv[1]
        currency_code_input = sys.argv[2]
    # 收集了中国银行外汇牌价网站所支持的所有货币
    currency_mapping = {
        "GBP": "英镑",
        "HKD": "港币",
        "USD": "美元",
        "CHF": "瑞士法郎",
        "DEM": "德国马克",
        "FRF": "法国法郎",
        "SGD": "新加坡元",
        "SEK": "瑞典克朗",
        "DKK": "丹麦克朗",
        "NOK": "挪威克朗",
        "JPY": "日元",
        "CAD": "加拿大元",
        "AUD": "澳大利亚元",
        "EUR": "欧元",
        "MOP": "澳门元",
        "PHP": "菲律宾比索",
        "THB": "泰国铢",
        "NZD": "新西兰元",
        "KRW": "韩国元",
        "RUB": "卢布",
        "MYR": "林吉特",
        "TWD": "新台币",
        "ESP": "西班牙比塞塔",
        "ITL": "意大利里拉",
        "NLG": "荷兰盾",
        "BEF": "比利时法郎",
        "FIM": "芬兰马克",
        "INR": "印度卢比",
        "IDR": "印尼卢比",
        "BRL": "巴西里亚尔",
        "AED": "阿联酋迪拉姆",
        "ZAR": "南非兰特",
        "SAR": "沙特里亚尔",
        "TRY": "土耳其里拉"
    }
    if currency_code_input not in currency_mapping:
        raise ValueError(f"不支持的货币代码: {currency_code_input}")
    scrape_forex_rate(date_input, currency_mapping[currency_code_input])