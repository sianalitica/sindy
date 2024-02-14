from libs import navigator,config
from libs.mysqli import mysqli
import re
from sindy.DocumentoInfo import DocumentoInfo
from typing import List

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

def saveDocs(list_docs:List[DocumentoInfo]):
    print("TOTAL: "+str(len(list_docs))+" de documentos")
    pass


def getDocs(nav:navigator.Navigator, total_docs_database) -> List[DocumentoInfo]:

    quantidadeRegistrosEl = nav.findElement("id", "grdDocumentos_info")
    matchQuant = re.search("([\d,]+)\sregistro", quantidadeRegistrosEl.getText())
    textQuant = matchQuant.group(1).replace(",", "")
    quantidade_total_do_site = int(textQuant)
    quantidade_registros_salvar = quantidade_total_do_site - int(total_docs_database)
    
    list_documents:List[DocumentoInfo] = []

    if(quantidade_registros_salvar > 0):

        total_raspados = 0

        index = ['codigo', 'empresa', 'categoria', 'tipo', 'especie', 'data_referencia', 'data_entrega', 'status', 'v', 'modalidade']
        
        finish = False

        while not finish:
            
            els = nav.findElements("css", "#grdDocumentos > tbody > tr")
            if(els == False): return list_documents

            for el in els:

                map_data = {
                    'codigo':'',
                    'empresa':'',
                    'categoria':'',
                    'tipo':'',
                    'especie':'',
                    'data_referencia':'',
                    'data_entrega':'',
                    'status':'',
                    'v':'',
                    'modalidade':'',
                    'link':''
                }

                html = el.getHTML()
                res  = re.search("onclick=\"OpenPopUpVer\(\'([^\s]+)\'\)\"\stitle", html)
                map_data['link'] = res.group(1)
                tds  = nav.findElements("tag", "td", 15, el)
                if tds == False: continue 

                i = 0
                max = len(tds) -1
                for td in tds:
                    map_data[index[i]] = td.getText()
                    i+=1
                    if i == max: break

                docObject = DocumentoInfo(map_data)
                docObject.to_string()
                list_documents.append(docObject)
                total_raspados += 1

                finish = quantidade_registros_salvar == total_raspados
                if finish: break
            # descomentar em produção
            """
            try:
                if not finish: 
                    nav.findElement('id', 'grdDocumentos_next').click()
                    nav.sleep(1)
            except:
                print('botão "seguinte" não está disponível para ser clicado')
            """

    return list_documents


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


def start():
    data_list = getDataInfo()
    for item in data_list:
        nav = navigator.Navigator(conf.getUrlCvmBase()+'frmConsultaExternaCVM.aspx?codigoCVM='+item[1])
        filter(nav)
        list_docs = getDocs(nav, item[2])
        saveDocs(list_docs)
        nav.sleep()
