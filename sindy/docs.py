from libs import config,mysqli
from libs.navigator import Navigator

conf = config.Config.instance()
conn = mysqli.mysqli.instance()

def configure_browser_download(browser, download_directory):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_directory}}
    browser.execute("send_command", params)

def download_file(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "/caminho/para/o/diretorio",  # Substitua pelo seu diretório de download desejado
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=chrome_options)

    configure_browser_download(driver, "/caminho/para/o/diretorio")

    driver.get(url)
    time.sleep(5)  # Aguarda um tempo para o download ser concluído
    driver.quit()

def getLinksDocsToAnalise():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            documentos_info.id as documentoinfo_id,
            documentos_info.link_documento
        from documentos_info
        where not documentos_info.id 
            in (
                select 
                   documentos_brutos.id 
                from
                   documentos_brutos 
            ) and not documentos_info.link_documento is null;
    """)
    return cursor.fetchall()

def read():
    # navi = navigator.Navigator(conf.getUrlCvmBase())

    links = getLinksDocsToAnalise()

    navigator = Navigator(conf.getUrlCvmBase()+links[0][1])
    iframe = navigator.findElement('tag', 'iframe')
    if iframe:
        navigator.sleep(1)
        blob = iframe.getValueOf('src')
        download_file(blob)
        #navigator.goto(blob, full=True)
        #navigator.sleep(1)
        #btnDownload = navigator.findElement('id', 'download')
        #print(btnDownload)
        
    navigator.sleep()

    print(conf.getUrlCvmBase())

    