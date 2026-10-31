import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import Base, engine, get_db
from . import models, schemas
from .security import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Prep Track API", version="1.0.0", description="Placement preparation planner API")
origins = [x.strip() for x in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"], allow_headers=["Authorization", "Content-Type"])

@app.get("/")
def root(): return {"message": "Prep Track API is running", "docs": "/docs"}
@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/auth/register", response_model=schemas.Token, status_code=201)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    email = data.email.lower()
    if db.query(models.User).filter(func.lower(models.User.email) == email).first():
        raise HTTPException(409, "An account with this email already exists")
    user = models.User(name=data.name.strip(), email=email, hashed_password=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    token = create_access_token(user.id)
    return {"access_token": token, "user": user}

@app.post("/auth/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(func.lower(models.User.email) == form.username.lower()).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Email or password is incorrect", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_access_token(user.id), "user": user}

@app.get("/auth/me", response_model=schemas.UserOut)
def me(user: models.User = Depends(get_current_user)): return user

@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    tasks = db.query(models.Task).filter_by(user_id=user.id)
    progress = db.query(models.Progress).filter_by(user_id=user.id).all()
    total = sum(p.total for p in progress); solved = sum(p.solved for p in progress)
    task_total = tasks.count()
    task_completed = tasks.filter_by(completed=True).count()
    task_pct = task_completed / task_total * 100 if task_total else None
    question_pct = solved / total * 100 if total else None
    available_scores = [score for score in (task_pct, question_pct) if score is not None]
    overall = round(sum(available_scores) / len(available_scores)) if available_scores else 0
    return {"task_total": task_total, "task_completed": task_completed, "topic_count": len(progress), "questions_solved": solved, "questions_total": total, "task_completion": round(task_pct) if task_pct is not None else 0, "question_completion": round(question_pct) if question_pct is not None else 0, "completion": overall}

@app.get("/tasks", response_model=list[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Task).filter_by(user_id=user.id).order_by(models.Task.created_at.desc()).all()
@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    item = models.Task(**data.model_dump(), user_id=user.id); db.add(item); db.commit(); db.refresh(item); return item
@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    item = db.query(models.Task).filter_by(id=task_id, user_id=user.id).first()
    if not item: raise HTTPException(404, "Task not found")
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    db.commit(); db.refresh(item); return item
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    item = db.query(models.Task).filter_by(id=task_id, user_id=user.id).first()
    if not item: raise HTTPException(404, "Task not found")
    db.delete(item); db.commit()

@app.get("/progress", response_model=list[schemas.ProgressOut])
def get_progress(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Progress).filter_by(user_id=user.id).order_by(models.Progress.id).all()
@app.post("/progress", response_model=schemas.ProgressOut, status_code=201)
def create_progress(data: schemas.ProgressCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if data.solved > data.total: raise HTTPException(400, "Solved count cannot exceed total")
    item = models.Progress(**data.model_dump(), user_id=user.id); db.add(item); db.commit(); db.refresh(item); return item
@app.patch("/progress/{progress_id}", response_model=schemas.ProgressOut)
def update_progress(progress_id: int, data: schemas.ProgressCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    item = db.query(models.Progress).filter_by(id=progress_id, user_id=user.id).first()
    if not item: raise HTTPException(404, "Progress topic not found")
    if data.solved > data.total: raise HTTPException(400, "Solved count cannot exceed total")
    for key, value in data.model_dump().items(): setattr(item, key, value)
    db.commit(); db.refresh(item); return item
@app.delete("/progress/{progress_id}", status_code=204)
def delete_progress(progress_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    item = db.query(models.Progress).filter_by(id=progress_id, user_id=user.id).first()
    if not item: raise HTTPException(404, "Progress topic not found")
    db.delete(item); db.commit()

@app.get("/materials", response_model=list[schemas.MaterialOut])
def get_materials(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Material).filter_by(user_id=user.id).order_by(models.Material.id.desc()).all()
@app.post("/materials", response_model=schemas.MaterialOut, status_code=201)
def create_material(data: schemas.MaterialCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not data.url.startswith(("https://", "http://")): raise HTTPException(400, "URL must start with http:// or https://")
    item = models.Material(**data.model_dump(), user_id=user.id); db.add(item); db.commit(); db.refresh(item); return item
@app.delete("/materials/{material_id}", status_code=204)
def delete_material(material_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    item = db.query(models.Material).filter_by(id=material_id, user_id=user.id).first()
    if not item: raise HTTPException(404, "Material not found")
    db.delete(item); db.commit()
