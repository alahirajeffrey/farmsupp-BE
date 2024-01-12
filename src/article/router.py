from fastapi import APIRouter, status, Depends, HTTPException, Query
from article import schemas
from database import get_db
import models
from sqlalchemy.orm import Session
import utils
from uuid import UUID
from profile.schemas import Role

router = APIRouter()

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.ArticleReturnSchema)
async def create_article(
    data: schemas.CreateArticleSchema, 
    db: Session = Depends(get_db),
    payload: dict = Depends(utils.validate_access_token)):

    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()

    if profile is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Profile does not exist"
        )

    if profile.role != Role.FARMER:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Only farmers can post articles"
        )


    new_article = models.Article(
        author_id= profile.id,
        body= data.body,
        title= data.title
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article

@router.get('/{article_id}', status_code=status.HTTP_200_OK, response_model=schemas.ArticleReturnSchema)
def get_single_article(
    article_id: str,
    db: Session = Depends(get_db),
    payload: dict = Depends(utils.validate_access_token)):

    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Article does not exist"
        )
    return article

@router.get('/author/{author_id}', status_code=status.HTTP_200_OK)
def get_all_user_articles(
    author_id: str,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Page number", gt=0),
    page_size: int = Query(10, description="Items per page", gt=0, le=100),
    payload: dict = Depends(utils.validate_access_token)):

    offset = (page - 1) * page_size

    # user_id_from_token = UUID(payload.get('sub'))
    # profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()

    profile_exists = db.query(models.Profile).filter(models.Profile.id == author_id).first()
    if not profile_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Author does not exist"
        )

    articles = db.query(models.Article).filter(models.Article.author_id == author_id).offset(offset).limit(page_size).all()

    if len(articles) == 0:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Author has not published any articles yet"
        )
    
    return articles

@router.delete('/{article_id}', status_code=status.HTTP_200_OK)
def delete_article(
    article_id: str,
    db: Session = Depends(get_db),
    payload: dict = Depends(utils.validate_access_token)):

    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Article does not exist"
        )
    
    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()
     
    if article.author_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot delete an article you do not own"
        ) 
    
    db.query(models.Article).filter(models.Article.id == article_id).delete()
    db.commit()

    return {"message":"Article deleted"}

@router.patch('/{article_id}', status_code=status.HTTP_200_OK, response_model=schemas.ArticleReturnSchema)
def update_article(
    article_id: str,
    data: schemas.ArticleUpdateSchema,
    db: Session = Depends(get_db),
    payload: dict = Depends(utils.validate_access_token)):

    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Article does not exist"
        )
    
    ## convert user id from payload to UUID
    user_id_from_token = UUID(payload.get('sub'))
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id_from_token).first()
     
    if article.author_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You cannot update an article you do not own"
        ) 
    
    if data.title is not None:
        article.title = data.title 
    if data.body is not None:
        article.body = data.body

    db.commit()
    db.refresh(article)

    return article
