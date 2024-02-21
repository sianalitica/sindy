from libs import navigator,config
from libs.mysqli import mysqli
import re
from sindy.DocumentoInfo import DocumentoInfo
from typing import List
from libs.navigator import Element
import json

from libs.logs import warning,danger,success

conf = config.Config.instance()


def generateLink(el:Element) -> tuple:

    html = el.getHTML()
    res  = re.search("OpenDownloadDocumentos\('([^\s]*)','([^\s]*)','([^\s]*)','([^\s]*)'\)", html)
        
    if res:
        valores = res.groups()
        return (f"frmDownloadDocumento.aspx?Tela=ext&numSequencia={valores[0]}&numVersao={valores[1]}&numProtocolo={valores[2]}&descTipo={valores[3]}&CodigoInstituicao=1", 1)
    else: 
        res  = re.search("VisualizaArquivo_ITR_DFP_IAN\('([^\s]*)','([^\s]*)','DOWNLOAD','([^\s]*)','([^\s]*)','([^\s]*)','([^\s]*)'\)", html)
        if not res:
            return ""
        valores = res.groups()
        return (f"download.asp?moeda={valores[5]}&tipo={valores[0]}&data={valores[1]}&razao={valores[2]}&site=C&ccvm={valores[4]}",2)


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


def saveDocs(list_docs:List[DocumentoInfo], empresa_id):
    
    if len(list_docs) == 0: return

    conn    = mysqli.instance()
    cursor  = conn.cursor()
    sqlstr  = "INSERT INTO documentos_info (empresa_id, categoria, tipo, especie, data_referencia, data_entrega, status, v, modalidade, link_documento, link_type) "
    sqlstr += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    datain  = []

    for doc in list_docs:
        doc.empresa_id = empresa_id
        datain.append(doc.get_row())
    try:
        cursor.executemany(sqlstr,datain)
        conn.commit()
        success("Total de "+str(len(list_docs))+" arquivos extraídos")
    except:
        danger('ERRO AO TENTAR SALVAR OS DADOS', "query -> "+sqlstr+"\n\ndata -> "+json.dumps(dict(datain)))
    


def getDocs(nav:navigator.Navigator, total_docs_database) -> List[DocumentoInfo]:

    quantidadeRegistrosEl = nav.findElement("id", "grdDocumentos_info")
    matchQuant = re.search("([\d,]+)\sregistro", quantidadeRegistrosEl.getText())
    textQuant = matchQuant.group(1).replace(",", "")
    quantidade_total_do_site = int(textQuant)
    quantidade_registros_salvar = quantidade_total_do_site - int(total_docs_database)
    
    list_documents:List[DocumentoInfo] = []
    page = 1

    if(quantidade_registros_salvar == 0):
        warning("Não há novos documentos à serem extraídos.")
        return list_documents

    if quantidade_registros_salvar < 0:
        danger(f"!!!! Há registros duplicados !!!! Total {abs(quantidade_registros_salvar)} registros !!!!")
        return list_documents
    
    total_raspados = 0

    index = ['codigo', 'empresa', 'categoria', 'tipo', 'especie', 'data_referencia', 'data_entrega', 'status', 'v', 'modalidade']
    
    finish = False

    while not finish:
        
        els = nav.findElements("css", "#grdDocumentos > tbody > tr")
        if(els == False): 
            danger("Não foi possível carregar a lista de documentos com '#grdDocumentos > tbody > tr' - extract: linha 97")
            return list_documents

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
                'link':'',
                'link_type':''
            }
            
            link_data = generateLink(el)
            map_data['link'] = link_data[0]
            map_data['link_type'] = link_data[1]
            
            tds  = nav.findElements("tag", "td", 15, el)
            if tds == False: continue 

            i = 0
            max = len(tds) -1
            for td in tds:
                map_data[index[i]] = td.getText()
                i+=1
                if i == max: break

            docObject = DocumentoInfo(map_data)
            list_documents.append(docObject)
            total_raspados += 1

            finish = quantidade_registros_salvar == total_raspados
            if finish: break
        
        try:
            if not finish: 
                nav.findElement('id', 'grdDocumentos_next').click()
                page+=1
                nav.sleep(1)
        except:
            danger('O botão "seguinte" não está disponível para ser clicado - extract: linha 142')

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
        saveDocs(list_docs, item[0])
