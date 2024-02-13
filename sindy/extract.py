"""

pega os dados primarios do site da cvm
faz uso do selenium para clicar nos botões, etc

"""

from libs import navigator,config
from libs.mysqli import mysqli

conf = config.Config.instance()

def getDataInfo():
    # vai ao banco de dados e retorna codigo cvm de cada cliente e a quantidade de documentos registrados em cada um
    cursor = mysqli.instance().cursor()
    cursor.execute("select * from empresas")
    myresult = cursor.fetchall()
    print(myresult)

def start():
    data = getDataInfo()
    nav = navigator.Navigator()
    pass


