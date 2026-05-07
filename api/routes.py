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

    return {'message': 'Login successful', 'role': db_user.role}

@router.post('/batches', response_model=schemas.Batch, status_code=201)
def create_batch(batch: schemas.Batch, db: Session = Depends(get_db)):
    existing = db.query(models.Batch).filter(models.Batch.code == batch.code).first()
    if existing:
        raise HTTPException(400, 'Batch code already in use')

    new_batch = models.Batch(
        code=batch.code,
        name=batch.name,
        year=batch.year,
        schedule=batch.schedule
    )

    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch

@router.get('/batches', response_model=List[schemas.Batch], status_code=200)
def get_batches(db: Session = Depends(get_db)):
    return db.query(models.Batch).all()

@router.get('/batches/{code}', response_model=schemas.Batch, status_code=200)
def get_batch(code: str, db: Session = Depends(get_db)):
    batch = db.query(models.Batch).filter(models.Batch.code == code).first()
    if not batch:
        raise HTTPException(404, 'Batch not found')
    return batch

@router.post('/notices', status_code=201)
def create_notice(notice: schemas.Notice, db: Session = Depends(get_db)):
    new_notice = models.Notice(
        text=notice.text,
    )
    db.add(new_notice)
    db.flush()

    for batch_code in notice.batches:
        batch = db.query(models.Batch).filter(models.Batch.code == batch_code).first()
        if not batch:
            raise HTTPException(404, f'Batch {batch_code} not found')
        db.add(models.NoticeBatch(notice_id=new_notice.id, batch_code=batch_code))

    db.commit()
    return {'message': 'Notice posted successfully'}

@router.get('/notices/{batch_code}', status_code=200)
def get_notices(batch_code: str, db: Session = Depends(get_db)):
    notice_batches = db.query(models.NoticeBatch).filter(models.NoticeBatch.batch_code == batch_code).all()
    notice_ids = [nb.notice_id for nb in notice_batches]
    notices = db.query(models.Notice).filter(models.Notice.id.in_(notice_ids)).all()
    return notices

@router.post('/results', status_code=201)
def create_result(result: schemas.Result, db: Session = Depends(get_db)):
    batch = db.query(models.Batch).filter(models.Batch.code == result.batch_code).first()
    if not batch:
        raise HTTPException(404, 'Batch not found')

    new_result = models.Result(
        title=result.title,
        description=result.description,
        total_marks=result.total_marks,
        batch_code=result.batch_code
    )
    db.add(new_result)
    db.flush()

    for score in result.scores:
        student = db.query(models.User).filter(models.User.name == score.name).first()
        if not student:
            raise HTTPException(404, f'Student {score.name} not found')
        db.add(models.StudentScore(
            result_id=new_result.id,
            student_id=student.id,
            marks=score.marks,
            remarks=score.remarks,
            absent=score.absent,
            seen_by_guardian=score.seen_by_guardian
        ))

    db.commit()
    return {'message': 'Results published successfully'}

@router.get('/results/{batch_code}', status_code=200)
def get_results(batch_code: str, db: Session = Depends(get_db)):
    return db.query(models.Result).filter(models.Result.batch_code == batch_code).all()

