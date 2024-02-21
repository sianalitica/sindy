from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

from libs.config import Config

def clearDirectory(temp_dir):
    files = os.listdir(temp_dir)
    for file in files:
        if file.lower() != 'readme.md':
            os.remove(temp_dir+file)

def downloadFinish(temp_dir):
    files = os.listdir(temp_dir)
    for file in files:
        if file.lower() != 'readme.md':
            return file.split('.')[-1] != 'crdownload' or "chrome" not in file.lower()


def download(link, typeLink):
    config     = Config.instance()
    temp_dir   = config.getTempDir()
    clearDirectory(temp_dir)
    typeLink   = int(typeLink)
    linkBase   = config.getUrlCvmBase() if typeLink == 1 else config.getLinkBase2()
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": temp_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    # chrome_options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(linkBase+link)
    while not downloadFinish(temp_dir):
        time.sleep(0.5)
    driver.quit()
    return True
