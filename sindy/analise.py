from libs.mysqli import mysqli
from libs.chatgpt import getAnaliseBy
from libs.logs import info,warning,success

import time

conn = mysqli.instance()

def getLastTextsToAnalise() -> str:
    
    sel = """
        select 
            documentos_brutos.id as doc_id,
            documentos_info.data_referencia
        from 
            documentos_brutos
        join
            documentos_info on documentos_brutos.documento_info_id = documentos_info.id
        where 
            documentos_info.categoria = 'Dados Econômico-Financeiros'
        and documentos_info.tipo = 'Press-release'
        and not
            documentos_brutos.id in (
                select 
                    distinct
                        dados_brutos_analisados_documentos.documento_bruto_id
                from dados_brutos_analisados_documentos
            )
        order by documentos_brutos.id limit 1;
    """

    cursor = conn.cursor()
    cursor.execute(sel)

    return cursor.fetchall()


def start():
    row = getLastTextsToAnalise()
    if len(row) == 0: 
        info("Não há dados a serem analisados")
        return
    text = row[0][1]
    total_char = len(row[0][1])
    if(total_char > 40000):
        wait = total_char / 40000
        init = 0
        while init < total_char:
            final = init+40000
            if final > total_char:
                final = total_char
            if final - init < 20000:
                init = final - 20000
            subtext = text[init:final]
            print(getAnaliseBy(subtext))
            init += 40000
            time.sleep(wait)
    else:
        print(getAnaliseBy(text))
        print("=========================================")
        # print(getAnaliseBy(text))
