from libs.mysqli import mysqli
from libs.chatgpt import getAnaliseBy
from libs.logs import info,warning,success,danger
import mysql.connector
import time
import math

conn = mysqli.instance()

def saveDataRow(documento_id, dado_bruto)-> bool:
    try:
        ins = """
            insert into dados_brutos_analisados_documentos
            (documento_bruto_id, dado_bruto) values (%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(ins, [documento_id, dado_bruto])
        conn.commit()
        print("1 dado foi salvo")
        return True
    except mysql.connector.Error as err:
        danger("Não foi possível salvar o dado bruto.", "mysql msg: "+err.msg+"\n mysql code: "+str(err.errno))
        return False
    

def saveMany(dados_brutos=[]):
    try:
        ins = """
            insert into dados_brutos_analisados_documentos
            (documento_bruto_id, dado_bruto) values (%s,%s)
        """
        cursor = conn.cursor()
        cursor.executemany(ins, dados_brutos)
        conn.commit()
        print(str(len(dados_brutos))+" dados foram salvos com sucesso")
        return True
    except mysql.connector.Error as err:
        danger("Não foi possível salvar os dados brutos.", "mysql msg: "+err.msg+"\n mysql code: "+str(err.errno))
        return False


def getLastTextsToAnalise() -> str:
    
    sel = """
        select 
            documentos_brutos.id as doc_id,
            documentos_brutos.texto as texto,
            documentos_info.data_referencia
        from 
            documentos_brutos
        join
            documentos_info on documentos_brutos.documento_info_id = documentos_info.id
        where 
            documentos_info.categoria = 'Dados Econômico-Financeiros'
        and documentos_info.tipo      = 'Press-release'
        and not
            documentos_brutos.id in (
                select 
                    distinct
                        dados_brutos_analisados_documentos.documento_bruto_id
                from dados_brutos_analisados_documentos
            )
        order by documentos_info.data_entrega desc limit 1;
    """

    cursor = conn.cursor()
    cursor.execute(sel)

    return cursor.fetchall()


def start():

    limit = 40000

    while True:

        row = getLastTextsToAnalise()

        if len(row) == 0: 
            info("Não há dados a serem analisados")
            break
        
        text = row[0][1]
        idrw = row[0][0]
        
        total_char = len(row[0][1])
        
        if(total_char > limit):
            
            wait = total_char / limit
            wait = math.ceil(60 / wait) + 20
            init = 0
            data = []

            while init < total_char:
                final = init+limit
                if final > total_char:
                    final = total_char
                if final - init < limit:
                    init = final - limit
                subtext = text[init:final]
                resp = getAnaliseBy(subtext)
                if resp == "context_length_exceeded":
                    limit = limit - 10000
                    continue
                if resp:
                    data.append((idrw,resp))
                    init += limit
                else: 
                    danger("O programa precisou ser parado por causa do erro anterior")
                    return False

                time.sleep(wait)
                
            if not saveMany(data):
                danger("O programa precisou ser parado por causa do erro anterior")
                return False
        else:
            resp = getAnaliseBy(text)
            if not saveDataRow(idrw, resp):
                danger("O programa precisou ser parado por causa do erro anterior")
                return False
            
        time.sleep(30)   

    return True
    
