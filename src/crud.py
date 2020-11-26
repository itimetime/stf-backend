from sqlalchemy.orm import Session

from . import models, schemas

# 创建case
def creat_case(db: Session, case: schemas.CaseIn, attachment):
    db_case = models.Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    if attachment:
        for i in attachment:
            db_attachment = db.query(models.Attachment).filter(models.Attachment.attachment_id == i).first()
            db_attachment.case_id = db_case.case_id
            db.commit()
    db.refresh(db_case)
    return db_case


def creat_attachment(db: Session, attachment: schemas.Attachment):
    db_attachment = models.Attachment(**attachment.dict())
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


# 获取case列表
def get_case_list(db: Session, skip: int, limit: int):
    return db.query(models.Case).offset(skip).limit(limit).all()


# 获取case详情
def get_case_detail(db: Session, case_id: int):
    # return db.query(models.Case).filter(models.Case.case_id == case_id).first()
    return db.query(models.Case).filter(models.Case.case_id == case_id).first()


# 更新case
def update_case(db: Session, case_id: int, case: schemas.CaseIn):
    db_case = db.query(models.Case).filter(models.Case.case_id == case_id).first()
    if db_case:
        update_dict = case.dict(exclude_unset=True)
        for k, v in update_dict.items():
            setattr(db_case, k, v)
        db.commit()
        db.flush()
        db.refresh(db_case)
        return db_case


# 删除case
def delete_case(db: Session, case_id: int):
    db_case = db.query(models.Case).filter(models.Case.case_id == case_id).first()
    if db_case:
        db.delete(db_case)
        db.commit()
        db.flush()
        return db_case


# 创建task
def creat_task(db: Session, task: schemas.Task):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# 获取task列表
def get_task_list(db: Session, skip: int, limit: int):
    return db.query(models.Task).offset(skip).limit(limit).all()


# 获取task详情
def get_task_detail(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.task_id == task_id).first()


# 获取apk列表 file_type 类型为1
def get_apk_list(db: Session, skip: int, limit: int):
    return db.query(models.Attachment).filter(models.Attachment.file_type == 1).offset(skip).limit(limit).all()