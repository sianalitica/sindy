from libs import config,mysqli
from libs.navigator import Navigator
from libs.driver_download import download
from libs.logs import info,warning,danger,success
from pypdf import PdfReader
import mysql.connector
import textract

import time
import json
import zipfile
import tarfile
import os
import subprocess

conf = config.Config.instance()
conn = mysqli.mysqli.instance()

"""
def converter_arquivos_pdf():

    direct = conf.getTempDir()
    files  = os.listdir(direct)
    
    for file in files:

        if file.lower() == "readme.md": continue
        if file.split(".")[-1] == 'pdf':
            with open("./docs_temp/"+file+'.html', "a+") as f:
                f.close()
            subprocess.run(["pdf2htmlEX", direct+file, './docs_temp/'+file+'.html'], bufsize=4096)
            # os.remove(direct+file)
         """   

def salvar_dados(documento_info_id, text, ext) -> bool:
    cursor  = conn.cursor()
    sqlstr  = "INSERT INTO documentos_brutos (documento_info_id, texto, ext) "
    sqlstr += "VALUES (%s, %s, %s)"
    datain  = (documento_info_id, text, ext)
    try:
        cursor.execute(sqlstr,datain)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        danger('ERRO AO TENTAR SALVAR OS DADOS EM documentos_brutos', "query -> "+sqlstr+"\n\ndata -> "+json.dumps(datain)+"\n\nmysql msg: "+err.msg+"\n mysql code: "+str(err.errno))
        return False


def ler_aquivo_qualquer(file) -> str:
    try:
        text = textract.process(file)
        return text
    except:
        try:
            with open(file, 'r', encoding = 'utf-8') as f:
                text = f.read()
                return text 
        except Exception as e:
            danger(f"Não foi possível ler o arquivo '{file}' | problema com encoding")
            return ""


def ler_arquivo_pdf(pdffile) -> str | None:
    try:
        reader = PdfReader(pdffile)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        danger("Não foi possível ler o arquivo pdf", f"msg: {e.msg}")
        return ler_aquivo_qualquer(pdffile)


def ler_arquivos_e_salvar(documento_info_id, files, dir) -> bool:

    total_success = 0
    total_error   = 0

    if len(files) <= 1: return salvar_dados(documento_info_id, "", "broken")

    for file in files:

        if file.lower() == "readme.md": continue
        extension = file.split(".")[-1]
        
        if os.path.isfile(dir+file):
            text = ler_arquivo_pdf(dir+file) if extension == 'pdf' else ler_aquivo_qualquer(dir+file)
            if salvar_dados(documento_info_id, text, extension):
                total_success += 1
            else: total_error += 1
        else:
            otherdir = dir+file+'/'
            othersfl = os.listdir(otherdir)
            ler_arquivos_e_salvar(documento_info_id, othersfl, otherdir)

    return total_success >= total_error



def extrair_arquivos(arquivo_compactado):

    destino  = conf.getTempDir()
    extensao = os.path.splitext(arquivo_compactado)[1].lower()

    if extensao in ('.zip', '.wtl'):
        with zipfile.ZipFile(destino+arquivo_compactado, 'r') as zip_ref:
            zip_ref.extractall(destino)
    elif extensao in ('.tar', '.gz', '.bz2', '.xz', '.tgz', '.tbz'):
        with tarfile.open(destino+arquivo_compactado, 'r:*') as tar_ref:
            tar_ref.extractall(destino)
    else:
        warning(f"Formato de arquivo '{extensao}' não suportado.")
    time.sleep(1)


def analise_arquivos():

    files = os.listdir(conf.getTempDir())

    for file in files:
        if file.lower() == "readme.md": continue
        if file.split('.')[-1].lower() in ('wtl','zip','tar','gz','bz2', 'xz', 'tgz', 'tbz'):
            extrair_arquivos(file)
            os.remove(conf.getTempDir()+file)
            


def getLinksDocsToAnalise():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            documentos_info.id as documentoinfo_id,
            documentos_info.link_documento,
            documentos_info.link_type
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

    links        = getLinksDocsToAnalise()
    successFiles = 0
    errorFiles   = 0

    if len(links) == 0:
        warning("Não há novos documentos a serem lidos e gravados")
        return
    
    info(f"Total de {str(len(links))} documentos a serem lidos e gravados")
    info(f"realizando downloads e armazenando os documentos brutos")
    
    errorLinks = ""
    for link in links:
        download(link=link[1], typeLink=link[2])
        analise_arquivos()
        maindir = conf.getTempDir()
        files   = os.listdir(maindir)
        if ler_arquivos_e_salvar(link[0], files, maindir):
            successFiles += 1
        else:
            errorLinks += f"| documento_info_id: {link[0]} , link: {link[1]} , type: {link[2]} |\n" 
            errorFiles += 1

    if successFiles > 0:
        success(f"{successFiles} arquivos foram lidos e salvos com sucesso")
    if errorFiles > 0:
        danger(f"Não foi possível ler ou salvar {errorFiles} arquivos")
    # converter_arquivos_pdf()
    

    