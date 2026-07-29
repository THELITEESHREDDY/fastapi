from fastapi import HTTPException,status

from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import session
from src.tasks.models import TaskModel







def create_task(task:TaskSchema, db:session):
    data = task.model_dump()

    new_task = TaskModel(title = data["title"],
                         description= data["description"],
                         is_completed = data["is_completed"]
                        )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)



    return {"status": "task created successfully...","data": new_task}



def get_tasks(db:session):
    tasks = db.query(TaskModel).all()

    return {"status": "All Tasks", "data":tasks}


def get_one_task(task_id:int, db:session):
    one_task = db.query(TaskModel).get(task_id)

    if not one_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Task id is incorrect {task_id}")
    
    return {"status":"Task Fetched Successfully", "data":one_task}