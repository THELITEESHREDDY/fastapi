from fastapi import APIRouter,Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db

task_routes = APIRouter(prefix="/task")


@task_routes.post("/create")
def create_task(task:TaskSchema, db = Depends(get_db)):
    return controller.create_task(task,db)



@task_routes.get("/{task_id}")
def get_one_task(task_id:int, db=Depends(get_db)):
    return controller.get_one_task(task_id,db)

@task_routes.get("/")
def get_all_tasks(db=Depends(get_db)):
    return controller.get_tasks(db)

