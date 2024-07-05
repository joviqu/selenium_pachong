import os

import requests
import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from weasyprint import HTML
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

proxies = [
    # 'https://proxy.server:4313',
    # 'https://proxy.server:4313',
    # 'https://proxy.server:4313'
]

def creat_chromedriver(proxies):
    """
    使用Selenium获取网页内容，以处理动态加载的内容。
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头浏览模式
    options.add_argument("--disable-gpu")
    options.add_argument("--windows-size=1920.1080")
    options.add_argument("--incognito")  # 无痕模式

    #代理
    proxy = random.choice(proxies)
    print(proxy)
    options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(options=options)
    return driver

def scroll_down(driver):
    time.sleep(10)  # 等待页面加载完成
    print("10s")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def fetch_web_content_with_selenium(url):
    # """
    # 使用Selenium获取网页内容，以处理动态加载的内容。
    # """
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 无头浏览模式
    # options.add_argument("--disable-gpu")
    # options.add_argument("--windows-size=1920.1080")
    # options.add_argument("--incognito")  # 无痕模式
    # #options.add_argument(f"user-agent={get_random_user_agent()}")
    #
    # #代理
    # proxy = random.choice(proxies)
    # print(proxy)
    # options.add_argument(f'--proxy-server={proxy}')
    #
    # # # 随机化浏览器窗口大小
    # # width, height = random.randint(800, 1920), random.randint(600, 1080)
    # # options.add_argument(f"--window-size={width},{height}")
    #
    #
    # driver = webdriver.Chrome(options=options)
    driver = creat_chromedriver(proxies)
    print(url)
    driver.get(url)
    time.sleep(10)  # 等待页面加载完成
    scroll_down(driver=driver)

    print("Successfully reached the bottom of the page!")
    # time.sleep(random.uniform(15, 20))

    content = driver.page_source
    driver.quit()
    return content


def fetch_and_convert_to_pdf(url, output_filename='output.pdf'):
    """
    抓取指定URL的网页内容，并将其转换为PDF文件。
    """
    # 使用Selenium获取网页内容
    html_content = fetch_web_content_with_selenium(url)

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 将BeautifulSoup对象转换回字符串，以便weasyprint处理
    html_string = str(soup.prettify())

    # 设置网页的base_url，确保图片等资源可以正确加载
    base_url = url if url.endswith('/') else url + '/'

    # 使用weasyprint将HTML字符串转换为PDF
    pdf_file = output_filename
    HTML(string=html_string, base_url=base_url).write_pdf(pdf_file)

    print(f"网页已成功转换为PDF并保存为: {pdf_file}")

# def fetch_and_save_as_html(url, output_filename='output.html'):
#     html_content = fetch_web_content_with_selenium(url)
#
#     if not html_content:
#         print("Failed to fetch html")
#         return
#
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     html_string = str(soup.prettify())
#
#     with open(output_filename, 'w', encoding='utf-8') as f:
#         f.write(html_string)
#     print(f"网页已成功保存为HTML文件: {output_filename}")

if __name__ == "__main__":
    target_url = "target_url"  # 请替换为目标网页URL
    fetch_and_convert_to_pdf(target_url)
    #fetch_and_save_as_html(target_url)