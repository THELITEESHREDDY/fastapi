from fastapi import HTTPException,status

from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from src.user.models import UserModel





def create_task(task:TaskSchema, db:Session, user:UserModel):
    data = task.model_dump()

    new_task = TaskModel(title = data["title"],
                         description= data["description"],
                         is_completed = data["is_completed"],
                         user_id = user.id
                        )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)



    return new_task


def get_tasks(db:Session,user:UserModel):
    tasks = db.query(TaskModel).filter(TaskModel.user_id==user.id).all()

    return tasks


def get_one_task(task_id:int, db:Session):
    one_task = db.query(TaskModel).get(task_id)

    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task id is incorrect {task_id}")
    
    return one_task

def update_task(body:TaskSchema, task_id:int, db:Session, user:UserModel):
    one_task:TaskModel = db.query(TaskModel).get(task_id)

    if not one_task:
        raise HTTPException(404, detail="Task id is incorrect")

    if one_task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to do this"
        )

    
    body= body.model_dump()

    for key,val in body.items():
        setattr(one_task,key,val)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return one_task


def delete_task(task_id:int,db:Session,user:UserModel):
    one_task:TaskModel = db.query(TaskModel).get(task_id)

    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="task id is incorrect"
                        )

    if one_task.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to do this"
            )

    
    db.delete(one_task)
    db.commit()

    return None