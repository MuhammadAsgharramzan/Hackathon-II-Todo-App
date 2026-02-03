from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from db.database import get_session
from models.task_model import Task, TaskCreate, TaskUpdate, TaskResponse
from auth.jwt_dependency import get_current_user, User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Create a new task for the authenticated user"""
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get all tasks for the authenticated user"""
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get a specific task by ID for the authenticated user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Update a specific task by ID for the authenticated user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Delete a specific task by ID for the authenticated user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/toggle-complete", response_model=TaskResponse)
async def toggle_task_completion(task_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Toggle the completion status of a task"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task