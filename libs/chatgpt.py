from libs.config import Config
import requests as request
import json
from libs.logs import danger,warning

text_patterm = """
    Sem justificar, pegue do texto os valores dos dados dos ítens baixo:

    Itens:

    - Data
    - Receita Líquida
    - EBITDA Ajustado
    - Resultado Financeiro Líquido
    - Resultado Líquido
    - Dívida Líquida
    - Dívida Líquida/EBITDA
    - Investimentos Total 

    Sobre o Item 'Data':
    O texto é uma demonstração dos resultados de uma data que pode conter a seguinte expressão regular: \d{1}[TtQq]\d{2}.

    Sbre o Item 'Dívida Líquida/EBITDA':
    Este item pode ser encontrado como 'Dívida Líq./EBITDA','Dívida Líq./EBITDA Ajustado' ou de outras formas


    Texto:
    
"""

def requestAnalise(token, texto):
    
    headers = {
        "Authorization":f"Bearer {token}",
        "Content-Type":"application/json"
    }

    texto = text_patterm + texto

    return request.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps({
        "model":"gpt-3.5-turbo",
        "messages":[
            {
                "role":"user",
                "content":texto
            }
        ]
    }))


def getAnaliseBy(texto):

    token = Config.instance().getChatGPTToken()

    if not token:
        return False

    req = requestAnalise(token, texto)
    
    if req.status_code != 200:
        
        warning("Não foi possível usar o token anterior para análise. Tentando com outro token agora.")

        while True:

            Config.instance().setNextToken()
            token = Config.instance().getChatGPTToken()

            if not token:
                danger("Não foi possível realizar a análise dos dados no chatgpt", "code: "+str(req.status_code)+" | msg: '"+req.text+"'")
                return False
                
            req = requestAnalise(token, texto)
            if req.status_code == 200: break

    
    resp = json.loads(req.text)
    return resp["choices"][0]["message"]["content"]
