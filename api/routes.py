from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
from database import get_db

router = APIRouter(prefix='/api')

@router.get('/users', response_model=List[schemas.UserResponse], status_code=200)
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get('/user/{user_id}', response_model=schemas.UserResponse, status_code=200)
def get_user_by_id(user_id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, 'User Not Found, make sure to register first')
    return user

@router.post('/register', response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.User, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing:
        raise HTTPException(400, 'Email already in use')

    if user.role == 'student':
        batch = db.query(models.Batch).filter(models.Batch.code == user.batch_code).first()
        if not batch:
            raise HTTPException(400, 'Invalid batch code')

    new_user = models.User(
        name=user.name,
        phone=user.phone,
        email=user.email,
        password=user.password,
        role=user.role,
        batch_code=user.batch_code if user.role == 'student' else None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login', status_code=200)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(404, "User doesn't exist")
    if user.password != db_user.password:
        raise HTTPException(400, 'Incorrect password')

    return {'message': 'Login successful', 'role': db_user.role, 'id': db_user.id}


@router.get('/batches', response_model=List[schemas.Batch], status_code=200)
def get_all_batches(db: Session = Depends(get_db)):
    return db.query(models.Batch).all()

@router.post('/new_batch/', response_model=schemas.Batch, status_code=201)
def create_new_batch(batch: schemas.Batch, db: Session = Depends(get_db)):
    db_teacher = db.query(models.User).filter(models.User.id == batch.teacher_id).first()
    if not db_teacher:
        raise HTTPException(404, 'Teacher Not Found')
    if db_teacher.role != 'teacher':
        raise HTTPException(403, 'Students are not allowed to create batches')
    
    new_batch = models.Batch(
        code=batch.code,
        name=batch.name,
        year=batch.year,
        schedule=batch.schedule,
        teacher_id=batch.teacher_id
    )

    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch

@router.get('/batches/{teacher_id}', response_model=List[schemas.Batch], status_code=200)
def get_batch_by_teacher_id(teacher_id, db: Session = Depends(get_db)):
    batches = db.query(models.Batch).filter(models.Batch.teacher_id == teacher_id)
    return batches

@router.get('/results', response_model=List[schemas.Result], status_code=200)
def get_all_results(db: Session = Depends(get_db)):
    return db.query(models.Result).all()

@router.get('/notices', response_model=List[schemas.Notice], status_code=200)
def get_all_results(db: Session = Depends(get_db)):
    return db.query(models.Notice).all()