from sqlalchemy import create_engine, text, Column, Integer, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.schema import ForeignKey

conn_url = 'postgresql://root:pass@db:5432/pg_database'  #Variable con el url de la base de datos

engine = create_engine(conn_url, pool_size=20, max_overflow=0)  
# Tipicamente se crea un engine por cada URL de una base de datos, se mantiene globalmente durante el proceso entero de la aplicación
# Un solo engine se encarga de administrar muchas connectiones individuales a la base de datos, está diseñado para ser invocado concurrentemente
# Es importante resaltar, que el engine es más efectivo cuando solo se crea uno al nivel modulo de la aplicación, no por cada objeto ni llamada de funcion
# El engine mantiene una referencia a un connection pool, de ahi salen referencias a las connectiones a la base de datos
# EL connection pooling está activado por default, sin embargo uno puede especifcar ciertos detalles al crear el engine, incluso negarlo

# Las conneciones son instancias del objeto 'Connection' del ORM, el cual es un objeto proxy para una verdadera DBPAI connection. Dicha conneción
# se recupera del connection pool y en donde se crea el objeto Connection

DBSession = sessionmaker(bind=engine) 
# Un session de SQL Alchemy establece todas las conversaciones del programa con la base de datos, provee una interfaz para queries donde retornan
# objetos mapeados de ORM. 
# El sessionmaker es un factory para los objetos de session con configuraciones establecidas, se le pasa un solo engine como parametro para tener una fuente de connexion
# Acá lo importante es resaltar que una vez que se emite un query dentro dentro de un session, le solicita un recurso de conneción del engine al cual el session está ligado
#Este session maker no crea sessions de la base de datos, si no del ORM que contiene configuraciones


Base = declarative_base()
# Acá se retorna un base class, todas las clases mapeadas deben heredar de el

# Relacion 1 a N
# Para dicha relación, se coloca un foreign key en la tabla secundaria que hace referencia a la principal (en este caso pets llevaria el foreign key del dueño, el user)
# Luego se especifica un 'relationship' en el objeto padre, como referencia a una colección de elementos representados por el hijo
# Esta relación ayuda en los joins

class users(Base):
    __tablename__ = 'users' # nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True)  # Primary key
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    petid = relationship('pets')  #relationship

    def __init__(self, firstname, lastname, age): # init del objeto
        self.firstname = firstname
        self.lastname = lastname
        self.age = age

class pets(Base):
    __tablename__ = 'pets' # nombre de la tabla en la base de datos
    
    id = Column(Integer, primary_key=True) # Primary key
    ownerid = Column(Integer, ForeignKey('users.id')) # Foreign key del dueño
    animaltype = Column(String)
    name = Column(String)

    def __init__(self, ownerid, animaltype, name): # init del objeto
        self.ownerid = ownerid
        self.animaltype = animaltype
        self.name = name



# Acá se instancia un session ya con un engine ligado, se utiliza con un with (Python context manager) y por lo tanto se cierra solo al final
# Transaccion que afecta a más de una tabla
with DBSession() as session:
    user1 = users(firstname='Oscar',lastname='Cerdas',age=25)
    session.add(user1)    # se agrega un registro a la tabla de users
    pet1 = pets(ownerid=4,animaltype='Horse',name='Speedy')
    session.add(pet1) # se agregua un registro a la tabla de pets
    session.commit()   # se hace un commit cuando se agregan datos a la session que deben ser actualizados


with DBSession() as session:
    usuarios = session.query(users).all()     

print('\n ##All Users: ')
for user in usuarios:
    print(f'{user.firstname} {user.lastname} is {user.age} years old')
print('')




# SQL Commands when creating database tables
#CREATE TABLE Users (
#id SERIAL,
#firstname VARCHAR(100),
#lastname VARCHAR(100),
#age INT,
#PRIMARY KEY(id)
#);

#CREATE TABLE Pets (
# id SERIAL,
# ownerid INT,
# animaltype VARCHAR(100),
# name VARCHAR(100),
# PRIMARY KEY(id),
# FOREGIN KEY (ownerid) REFERENCES Users(id) ON DELETE CASCADE
#);


