
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, Column, Integer, Date, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

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
    pets = relationship('pets')  #relationship

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
