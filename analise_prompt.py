from libs.mysqli import mysqli
from libs.logs import success,warning,info,header,clear


class DataDoc:

    id = 0
    dado = ""
    regex = "-\s((Receita Líquida|EBITDA Ajustado|Resultado Financeiro Líquido|Resultado Líquido|Dívida Líquida|Dívida Líquida\/EBITDA|Investimentos Total)[:\/\s]*)\n(\s+-\s([^\n]+)\n)+"
    hasback = 0

    def __init__(self):
        
        cursor = conn.cursor()
        cursor.execute("select id, dado_bruto from dados_brutos_analisados_documentos order by id asc limit 1")
        
        result    = cursor.fetchall()

        if len(result) > 0:
            self.id   = result[0][0]
            self.dado = result[0][1]


conn = mysqli.instance()
data = DataDoc()

def init():

    while True:

        header("Analise de dados", False)
        info("Digite o comando 'start', 'sair' ou o id do dado bruto a ser analisado")
        if not main_command(input()): break
        clear()
        
        if data.id == 0: 
            warning("Não há documentos para analisar")
            break

        while True:
            setRow()
            success("""
                ID DOCUMENTO: """+str(data.id)+"""
            """)
            info("Digite o comando de analise:")
            warning("""
                Comandos:
                    - regex: para verificar se os dados estão sendo resgatados
                    - dado: para analisar o dado
                    - next: para o proximo registro
                    - back: para voltar ao registro anterior
                    - sair: para voltar ao menu principal
            """)
            if sub_command(input()):
                continue 
            break


def setRow(id=0):
    if id <= 0 and data.id <= 0:
        warning("Não foi encontrado o documento com o id "+str(id))
        return
    idf = id if id > 0 else data.id 
    cursor = conn.cursor()
    cursor.execute("select id, dado_bruto from dados_brutos_analisados_documentos where id = "+str(idf))
    result = cursor.fetchall()
    if len(result) > 0:
        data.id = result[0][0]
        data.dado = result[0][1]
    else: warning("Não foi encontrado o documento com o id "+str(id))


def setNext():
    data.id      = data.id + 1
    data.hasback = data.hasback + 1


def setBack():
    if data.hasback - 1 >= 0:
        data.id = data.id - 1
        data.hasback = data.hasback - 1
    return True





def main_command(comand):
    if comand == "start":
        return True
    else:
        clear()
        success("Até breve!")
        return False 


def sub_command(comand):
    
    if comand == "sair":
        clear()
        return False
    
    if comand == "next":
        setNext()
        clear()
        return True
    
    if comand == "back":
        setBack()
        clear()
        return True
    
    if comand == "dado":
        clear()
        print(data.dado)
        print("--------------------------------------------------------------------------")
        info("digite qualquer coisa para sair....")
        print("--------------------------------------------------------------------------")
        input()
        clear()
        return True
    
    return True

init()

