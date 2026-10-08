from sqlalchemy import Column , String , Integer , Boolean
from database import Base 

class Todo(Base):
    __tablename__= "todos"

    id = Column(Integer , primary_key=True , index= True )
    title = Column(String ,nullable=False )
    description = Column(String , nullable=True)
    completed = Column(Boolean , default=False)
    priority = Column(Integer , default=1)




