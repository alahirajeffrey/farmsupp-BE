from fastapi import APIRouter, status

router = APIRouter()

@router.post('', status_code=status.HTTP_201_CREATED)
def register_user():
    return {"message":"user registered"}