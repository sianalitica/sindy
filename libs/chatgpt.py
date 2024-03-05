from libs.config import Config
import requests as request
import json

TOKEN = Config().getChatGPTToken()

headers = {
    "Authorization":f"Bearer {TOKEN}",
    "Content-Type":"application/json"
}

text_patter_data = "O documento abaixo contém dados que fazer referência à uma data que pode estar com a seguinte expressão regular: \d{1}[TtQq]\d{2}"


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

    if req.status_code != 200:
        return False
    
    resp = json.loads(req.text)
    return resp["choices"][0]["message"]["content"]
