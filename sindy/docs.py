from libs import config,mysqli
from libs.navigator import Navigator

conf = config.Config.instance()
conn = mysqli.mysqli.instance()


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
    # navi = Navigator(conf.getUrlCvmBase())
    
    links = getLinksDocsToAnalise()
    if len(links) == 0: return
    navigator = Navigator(conf.getUrlCvmBase()+links[0][1])
    #iframe = navigator.findElement('tag', 'iframe')
   # if iframe:
     #   navigator.sleep(1)
     #   blob = iframe.getValueOf('src')
        # download_file(blob)
        # navigator.goto(blob, full=True)
        # navigator.sleep(1)
        # btnDownload = navigator.findElement('id', 'download')
        # print(btnDownload)
        
    navigator.sleep()

    #print(conf.getUrlCvmBase())

    