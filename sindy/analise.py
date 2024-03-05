from libs.mysqli import mysqli
from libs.chatgpt import getAnaliseBy
from libs.logs import info,warning,success,danger
import mysql.connector
import time

conn = mysqli.instance()

# -\s((Receita Líquida|EBITDA Ajustado|Resultado Financeiro Líquido|Resultado Líquido|Dívida Líquida|Dívida Líquida\/EBITDA|Investimentos Total)[:\/\s]*)\n(\s+-\s([^\n]+)\n)+

def saveDataRow(documento_id, dado_bruto)-> bool:
    try:
        ins = """
            insert into dados_brutos_analisados_documentos
            (documento_bruto_id, dado_bruto) values (%s,%s)
        """
        cursor = conn.cursor()
        cursor.execute(ins, [documento_id, dado_bruto])
        conn.commit()
        # print("um dado foi salvo")
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
        # print(str(len(dados_brutos))+" dados foram salvos com sucesso")
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

    while True:

        row = getLastTextsToAnalise()

        if len(row) == 0: 
            info("Não há dados a serem analisados")
            break
        
        text = row[0][1]
        idrw = row[0][0]
        
        total_char = len(row[0][1])
        
        if(total_char > 40000):
            
            wait = total_char / 40000
            wait = 60 / wait
            init = 0
            data = []

            while init < total_char:
                final = init+40000
                if final > total_char:
                    final = total_char
                if final - init < 20000:
                    init = final - 20000
                subtext = text[init:final]
                resp = getAnaliseBy(subtext)
                if resp:
                    data.append((idrw,resp))
                    init += 40000
                time.sleep(wait)
                
            if not saveMany(data):
                danger("O programa precisou ser parado por causa do erro anterior")
                return False
        else:
            if not saveDataRow(idrw, text):
                danger("O programa precisou ser parado por causa do erro anterior")
                return False
            
        time.sleep(30)   

    return True
    
