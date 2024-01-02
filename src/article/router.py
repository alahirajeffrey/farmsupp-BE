from fastapi import APIRouter, status

router = APIRouter()

@router.post('', status_code=status.HTTP_201_CREATED)
def create_article():
    return {"message":"article created"}

@router.get('/{article_id}', status_code=status.HTTP_200_OK)
def get_single_article():
    return {"message":"article"}

@router.get('/{user_id}', status_code=status.HTTP_200_OK)
def get_all_user_articles():
    return {"message":"article"}

@router.delete('/{article_id}', status_code=status.HTTP_200_OK)
def delete_article():
    return {"message":"article"}

@router.patch('/{article_id}', status_code=status.HTTP_200_OK)
def update_article():
    return {"message":"article"}
