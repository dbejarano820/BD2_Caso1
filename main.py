from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from engine import motor
from tables import users, pets

# Tipicamente se crea un engine por cada URL de una base de datos, se mantiene globalmente durante el proceso entero de la aplicación
# Un solo engine se encarga de administrar muchas connectiones individuales a la base de datos, está diseñado para ser invocado concurrentemente
# Es importante resaltar, que el engine es más efectivo cuando solo se crea uno al nivel modulo de la aplicación, no por cada objeto ni llamada de funcion
# El engine mantiene una referencia a un connection pool, de ahi salen referencias a las connectiones a la base de datos
# EL connection pooling está activado por default, sin embargo uno puede especifcar ciertos detalles al crear el engine, incluso negarlo

# Las conneciones son instancias del objeto 'Connection' del ORM, el cual es un objeto proxy para una verdadera DBPAI connection. Dicha conneción
# se recupera del connection pool y en donde se crea el objeto Connection

DBSession = sessionmaker(bind=motor.getInstance().engine) 
# Un session de SQL Alchemy establece todas las conversaciones del programa con la base de datos, provee una interfaz para queries donde retornan
# objetos mapeados de ORM. 
# El sessionmaker es un factory para los objetos de session con configuraciones establecidas, se le pasa un solo engine como parametro para tener una fuente de connexion
# Acá lo importante es resaltar que una vez que se emite un query dentro dentro de un session, le solicita un recurso de conneción del engine al cual el session está ligado
#Este session maker no crea sessions de la base de datos, si no del ORM que contiene configuraciones

# Relacion 1 a N
# Para dicha relación, se coloca un foreign key en la tabla secundaria que hace referencia a la principal (en este caso pets llevaria el foreign key del dueño, el user)
# Luego se especifica un 'relationship' en el objeto padre, como referencia a una colección de elementos representados por el hijo
# Esta relación ayuda en los joins


# Acá se instancia un session ya con un engine ligado, se utiliza con un with (Python context manager) y por lo tanto se cierra solo al final
# Transaccion que afecta a más de una tabla
with DBSession() as session:
    try:
        user1 = users(firstname='Oscar',lastname='Cerdas',age=25)
        session.add(user1)    # se agrega un registro a la tabla de users
        pet1 = pets(ownerid=4,animaltype='Horse',name='Speedy')
        session.add(pet1) # se agregua un registro a la tabla de pets
        session.commit()   # se hace un commit cuando se agregan datos a la session que deben ser actualizados
    except:
        session.rollback()
    
# Previamente se le habia metido datos a la base

with DBSession() as session:
    usuarios = session.query(users).all()     

print('\n ##All Users: ')
for user in usuarios:
    print(f'{user.firstname} {user.lastname} is {user.age} years old')
print('')


with DBSession() as session:   #Select para validar la relacion 1 a N
    result = session.execute(
        select(users.firstname, pets.animaltype, pets.name).join(users.pets).order_by(users.id, pets.id)
    )

for row in result:
    print(f' The user: {row.firstname}   has a {row.animaltype} named {row.name}')

    

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


