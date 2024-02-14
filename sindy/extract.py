from libs import navigator,config
from libs.mysqli import mysqli


conf = config.Config.instance()


def getDataInfo():
    cursor = mysqli.instance().cursor()
    cursor.execute("""
        SELECT 
            empresas.id as emp_id,
            empresas.cod_cvm as cod,
            (
                SELECT count(*) 
                FROM   documentos_info
                WHERE  documentos_info.empresa_id = emp_id
            ) as  total
            from empresas;
    """)
    return cursor.fetchall()


def getDocs(nav:navigator.Navigator, total_docs_database):
    # pega o elemento com o texto de registro na base da tabela usando o <div id = grdDocumentos_info>
    # o texto terá "Mostrando de 1 até 100 de 2,664 registros"
    # criar o regex para puxar a quantidade total
    # comparar a quantidade_total_do_site < total_docs_database para saber quantos registros precisamos pegar 
    # pega os registros
    # clica em seguinte se for necessário
    # salva os registros no banco de dados
    pass


def filter(nav:navigator.Navigator):
    
    nav.sleep(2)
    
    input = nav.findElement("id", "rdPeriodo")
    if input: input.click()
    
    dataini = nav.findElement("id", "txtDataIni")
    if dataini:
        dataini.click()
        dataini.value("01/01/1994")

    btn = nav.findElement("id", "btnConsulta")
    if btn: btn.click()
    
    els = []
    while len(els) == 0:
        els = nav.findElements("css", "#grdDocumentos > tbody > tr")
        nav.sleep(1)

    linkSemAssunto = nav.findElement("id", "lnkSemAssunto")
    if linkSemAssunto: linkSemAssunto.click()

    nav.sleep()


def start():
    data_list = getDataInfo()
    for item in data_list:
        nav = navigator.Navigator(conf.getUrlCvmBase()+'frmConsultaExternaCVM.aspx?codigoCVM='+item[1])
        filter(nav)
        getDocs(nav, item[2])
