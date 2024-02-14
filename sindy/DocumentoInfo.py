import re

def data_dia_mes(data) -> str:
    dataMesParts = data.split('/')
    return dataMesParts[2]+'-'+dataMesParts[1]+'-'+(dataMesParts[0] if len(dataMesParts[0]) == 2 else '0'+dataMesParts[0])

def transform_data_full(data) -> str:
    parts = data.split()
    return data_dia_mes(parts[0])+' '+parts[1]+':00'

def transform_data_dia_mes(data) -> str:
    return data_dia_mes(data)+' 00:00:00'

def transform_data_mes(data) -> str:
    dataMesParts = data.split('/')
    return dataMesParts[1]+'-'+dataMesParts[0]+'-01 00:00:00'

def get_status(status) -> int:
    if(status.lower() == 'ativo'):
        return 1
    elif(status.lower() == 'inativo'):
        return 2
    else: return 3

class DocumentoInfo:
    
    codigo=''
    empresa=''
    categoria=''
    tipo=''
    especie=''
    data_ref=''
    data_ent=''
    status=3 # 1 - ativo | 2 - inativo | 3 - indefinido 
    v=0
    modalidade=''
    link=''

    def __init__(self, map_doc:map):
        
        self.codigo     = map_doc['codigo'].strip()
        self.empresa    = map_doc['empresa'].strip()
        self.categoria  = map_doc['categoria'].strip()
        self.link       = map_doc['link'].strip()
        
        self.tipo       = '-' if map_doc['tipo'].strip()       == '' else map_doc['tipo'].strip()
        self.especie    = '-' if map_doc['especie'].strip()    == '' else map_doc['especie'].strip()
        self.modalidade = '-' if map_doc['modalidade'].strip() == '' else map_doc['modalidade'].strip()
        self.v          = 0   if map_doc['v'].strip()          == '' else int(map_doc['v'])
        
        self.data_ref   = DocumentoInfo.data_to_en(map_doc['data_referencia'])
        self.data_ent   = DocumentoInfo.data_to_en(map_doc['data_entrega'])
        self.status     = get_status(map_doc['status'])


    def data_to_en(data) -> str:

        if re.match("\d{1,2}\/\d{2}\/\d{4}\s\d{2}:\d{2}", data):
            return transform_data_full(data)

        if re.match("\d{1,2}\/\d{2}\/\d{4}", data):
            return transform_data_dia_mes(data)
        
        if re.match("\d{2}\/\d{4}", data):
            return transform_data_mes(data)
        else:
            return "0000-00-00 00:00:00"
        
    def to_string(self):
        print({
            'codigo':self.codigo,
            'empresa':self.empresa,
            'categoria':self.categoria,
            'tipo':self.tipo,
            'data_ref':self.data_ref,
            'data_ent':self.data_ent,
            'status':self.status,
            'v':self.v,
            'modalidade':self.modalidade,
            'link':self.link,
        })