from libs import config,mysqli
from libs.navigator import Navigator
from libs.driver_download import download
from libs.logs import info,warning
from pypdf import PdfReader

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

def salvar_dados():
    pass

def ler_arquivo_pdf(pdffile) -> str:
    reader = PdfReader(pdffile)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def ler_arquivos_e_salvar():

    files = os.listdir(conf.getTempDir())

    for file in files:
        if file.lower() == "readme.md": continue
        extension = file.split(".")[-1]
        if extension == 'pdf':
            text = ler_arquivo_pdf(conf.getTempDir()+file)
        else:
            text = ""
        
        salvar_dados()

def extrair_arquivos(arquivo_compactado):

    destino  = conf.getTempDir()
    extensao = os.path.splitext(arquivo_compactado)[1].lower()

    if extensao in ('.zip', '.WTL'):
        with zipfile.ZipFile(destino+arquivo_compactado, 'r') as zip_ref:
            zip_ref.extractall(destino)
    elif extensao in ('.tar', '.gz', '.bz2', '.xz', '.tgz', '.tbz'):
        with tarfile.open(destino+arquivo_compactado, 'r:*') as tar_ref:
            tar_ref.extractall(destino)
    else:
        warning(f"Formato de arquivo '{extensao}' não suportado.")


def analise_arquivos():

    files = os.listdir(conf.getTempDir())

    for file in files:
        if file.lower() == "readme.md": continue
        if file.split('.')[-1] in ('WTL','zip','tar','gz','bz2', 'xz', 'tgz', 'tbz'):
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

    links = getLinksDocsToAnalise()
    
    if len(links) == 0:
        warning("Não há novos documentos a serem lidos e gravados")
        return
    info(f"Total de {str(len(links))} documentos a serem lidos e gravados")
    info(f"realizando downloads e armazenando os documentos brutos")
    # download(link=links[0][1], typeLink=links[0][2])
    # analise_arquivos()
    # converter_arquivos_pdf()
    ler_arquivos_e_salvar()

    