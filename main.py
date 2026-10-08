from database import engine , Base , SessionLocal
import models , schemas
from fastapi import FastAPI , Depends  , HTTPException
from sqlalchemy.orm import Session 
from auth import verify_token , create_token 




app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db =  SessionLocal()
    try: 
        yield db 
    finally:
        db.close()

#login
@app.post("/login")
def login_api():
    return {
        "access_token" : create_token({"user" : 'admin'}),
        "token_type" : "bearer"
    }

#create (protected)
@app.post("/todos" , response_model=schemas.TodoResponse)
def create_todo(todo : schemas.TodoCreate , db: Session = Depends(get_db), user =  Depends (verify_token)):

    new_todo = models.Todo(
        title = todo.title,
        description = todo.description,
        completed = todo.completed,
        priority = todo.priority

     )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo 


#read all 
@app.get("/todosall" ,  response_model=list[schemas.TodoResponse])
def real_all (db : Session = Depends(get_db)):

    todos = db.query(models.Todo).all()

    if not todos :
        raise HTTPException(
            status_code=404,
            detail="todo not found"
        )

    return todos



#read one nby one
@app.get("/readone/{id}", response_model=schemas.TodoResponse )
def read_one (id : int , db : Session = Depends(get_db)):

    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo :
        raise HTTPException(
            status_code=404,
            detail="todo not found"
        )

    return todo

@app.put("/update/{id}",response_model=schemas.TodoResponse)

def update_one(
    id : int,
    todo_data : schemas.TodoCreate,
    db : Session = Depends(get_db),
    data = Depends(verify_token)
):

    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo : 
        raise HTTPException(
            status_code=404,
            detail="toos not found"
        )

    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed
    todo.priority = todo_data.priority

    db.commit()
    db.refresh(todo)

    return todo

@app.get("/todo")
def read_todo():
    return {
        "message" : "todo working sucessfully "
    }

#delete todo api 
@app.delete("/deleteTodo/{id}")
def delete_todo(id : int , db : Session = Depends(get_db)):

    todo = db.query(models.Todo).filter(models.Todo.id == id).first()

    if not todo :
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )

    db.delete(todo)
    db.commit()

    return {
        "message" : "todo deleted sucessfully"
    }









    



