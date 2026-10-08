from pydantic import BaseModel 



class TodoCreate(BaseModel):
    title : str 
    description : str | None = None
    completed : bool = False
    priority : int = 1 

class TodoResponse(BaseModel):

    id : int
    title : str 
    description : str | None = None
    completed : bool 
    priority : int 


    class Config :
        from_attributes = True 





