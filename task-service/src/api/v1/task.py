from src.models.task import Task
from src.services.task import TaskService, get_task_service
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/health")
async def get_health() -> dict:
    return {"message": "ok"}


@router.post("/create_task")
async def publish_task_info(
        task: Task,
        task_service: TaskService = Depends(get_task_service)
) -> dict:
    data_key = await task_service.store_task_data_to_cache(
        task.json(include={"data"})
    )
    await task_service.publish_task_config(task, data_key)
    return {
        "status": "success",
        "task_name": task.name,
        "data_key": data_key,
    }
