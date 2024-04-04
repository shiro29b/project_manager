

from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db
from .. import models,schemas,utils,oauth2
from fastapi import Depends,status , HTTPException, APIRouter


router =  APIRouter(
    prefix="/project",
    tags=["Projects"]
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate, current_user : int =Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    # Checking if current user has permission to create projects
    if current_user.role not in ["SuperAdmin", "Admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to create projects")
    # Check if manager is valid
    project_manager = db.query(models.User).filter(models.User.id == project.project_manager_id).first()
    if project_manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project manager not found")
    if project_manager.role not in ["SuperAdmin", "Admin"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project manager must be an Admin or SuperAdmin")

    # Check if client_id is valid
    client = db.query(models.User).filter(models.User.id == project.client_id).first()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if client.role != "Client":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client must have role 'Client'")

    #avoiding projet duplication
    existing_project = db.query(models.Project).filter(models.Project.name == project.name).first()
    if existing_project:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A project with the same name already exists")

    
   
    project_db = models.Project(**project.model_dump())
    db.add(project_db)
    db.commit()
    db.refresh(project_db)
    return project_db


@router.delete("/{id}")
def delete_project(id:int,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    # Check if current user has permission to delete projects
    if current_user.role != "SuperAdmin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete projects")

    # Commented out logic for deleting project
    project_db = db.query(models.Project).filter(models.Project.id == id)
    if project_db.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    project_db.delete(synchronize_session=False)
    db.commit()

    return {"message": "Project deleted successfully"}

    

@router.put("/{id}",response_model=schemas.ProjectOut)
async def update_project(id: int, project: schemas.ProjectCreate,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    if current_user.role not in ["SuperAdmin", "Admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update projects")
    #check if project exists
    project_db = db.query(models.Project).filter(models.Project.id == id)
    if project_db.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    # Check if manager is valid
    project_manager = db.query(models.User).filter(models.User.id == project.project_manager_id).first()
    if project_manager is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project manager not found")
    if project_manager.role not in ["SuperAdmin", "Admin"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project manager must be an Admin or SuperAdmin")

    # Check if client_id is valid
    client = db.query(models.User).filter(models.User.id == project.client_id).first()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if client.role != "Client":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client must have role 'Client'")

    #if name is changed , the name cannot be as that of existing projects but if not updating then can be the same
    existing_project = db.query(models.Project).filter(models.Project.name == project.name).first()
    if existing_project.id!= id and existing_project.name==project.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A project with the same name already exists")
    
    project_db.update(project.model_dump(),synchronize_session=False)
    db.commit()
    return project_db.first()


@router.get("/",response_model=List[schemas.ProjectOut])
def getProjects( db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    if current_user.role == "SuperAdmin" or current_user.role == "Admin":
        projects = db.query(models.Project).all()
    else:
        projects = db.query(models.Project).filter(models.Project.client_id == current_user.id).all()
    return projects


    





