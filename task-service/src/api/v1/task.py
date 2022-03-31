from src.models.task import Task
from src.services.task import TaskService, get_task_service
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/health")
async def get_health() -> dict:
    return {"message": "ok"}


@router.post("/create_task")
async def publish_task_info(task: Task, task_service: TaskService = Depends(get_task_service)):
    task_key = await task_service.publish_task_config(task)
    return {
        "status": "success",
        "task": task.dict(),
        "task_key": task_key,
    }
