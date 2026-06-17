from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user, require_roles
from app.models import Camera, User, UserRole
from app.schemas import CameraCreate, CameraRead, CameraUpdate

router = APIRouter(tags=["Cameras"])


@router.get("/cameras", response_model=list[CameraRead])
def list_cameras(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Camera).order_by(Camera.id).all()


@router.post("/camera", response_model=CameraRead, status_code=status.HTTP_201_CREATED)
def create_camera(payload: CameraCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.manager))):
    camera = Camera(**payload.model_dump())
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera


@router.put("/camera/{camera_id}", response_model=CameraRead)
def update_camera(
    camera_id: int,
    payload: CameraUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.manager)),
):
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(camera, key, value)
    db.commit()
    db.refresh(camera)
    return camera


@router.delete("/camera/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(camera_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    db.delete(camera)
    db.commit()
