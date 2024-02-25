from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

from libs.config import Config

def clearDirectory(temp_dir):
    files = os.listdir(temp_dir)
    for file in files:
        if file.lower() != 'readme.md':
            if os.path.isfile(temp_dir+file):
                os.remove(temp_dir+file)
            else: 
                clearDirectory(temp_dir+file+"/")
                os.rmdir(temp_dir+file)

def downloadFinish(temp_dir):
    files = os.listdir(temp_dir)
    if len(files) <= 1: return True
    for file in files:
        if file.lower() != 'readme.md':
            for word in ("chrome", "crdownload"):
                if word in file.lower():
                    return False
            return True

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
    chrome_options.add_argument('--headless=new')
    driver = safe_driver(chrome_options, linkBase+link)
    time.sleep(1)
    while not downloadFinish(temp_dir):
        time.sleep(0.5)
    time.sleep(1)
    driver.quit()
    return True


def safe_driver(options, link):
    while True:
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(link)
            return driver
        except:
            time.sleep(1)
            continue
