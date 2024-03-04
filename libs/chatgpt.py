from libs.config import Config
import requests as request
import json

TOKEN = Config().getChatGPTToken()

headers = {
    "Authorization":f"Bearer {TOKEN}",
    "Content-Type":"application/json"
}


text_patterm = """
    Sem justificar, pegue do texto os dados dos ítens exibindo os subitens da seguinte forma:

    - item:
        - data 
        - valor 
        - contexto do valor
        - tipo de valor (real ou dolar) 

    Itens:

    - Receita Líquida
    - EBITDA Ajustado
    - Resultado Financeiro Líquido
    - Resultado Líquido
    - Dívida Líquida
    - Dívida Líquida/EBITDA
    - Investimentos Total 

    Detalhes:

    Se não tiver algum item, adicione o dado 'nulo' para ele sem exibir os subitens.
    O valor pode ser qualquer tipo numerico ou texto
    As datas podem ter a seguinte expressão regular: \d{1}[TtQq]\d{2}.
    transforme outros tipos de datas para o padrão brasileiro (dd/mm/YYYY)
    contexto do valor porde ser milhões, mil, bilhões ou outro tipo se for identificado 
    tipo de valor pode ser real, dolar ou nulo caso não seja identificado
    Pode haver mais de um valor para cada item especificado em datas distintas. 
    É necessário tentar pegar todos os valores e datas em cada ítem

    Texto:
    
"""

def getAnaliseBy(texto):

    texto = text_patterm + texto

    req = request.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps({
        "model":"gpt-3.5-turbo",
        "messages":[
            {
                "role":"user",
                "content":texto
            }
        ]
    }))

    # print(req.status_code )
    # print(req.text )

    if req.status_code != 200:
        return False
    
    resp = json.loads(req.text)
    return resp["choices"][0]["message"]["content"]
