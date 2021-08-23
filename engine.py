
from sqlalchemy import create_engine 

#Clase singleton que se encarga de asegurar que solamente un engine se crea, esto para controlar el tema de las llamadas
class motor:
    __instance = None
    conn_url = 'postgresql://root:pass@db:5432/pg_database'  #Variable con el url de la base de datos
    engine = create_engine(conn_url, pool_size=20, max_overflow=0)     #Configuraciones del connection pool 
    @staticmethod
    def getInstance():
        if motor.__instance == None:
            motor()
        return motor.__instance
    
    def __init__(self):
        if motor.__instance != None:
            raise Exception("Es un singleton!")
        else:
            motor.__instance = self
