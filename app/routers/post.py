from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, Response , status, APIRouter
from .. database import  engine, get_db
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(prefix="/posts",
                   tags=['posts'])


@router.get("/",response_model=List[schemas.PostOut])  
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit : int=10, skip :int=0, search: Optional[str]= ""):
    
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
   # cursor.execute("""SELECT * FROM posts""")
   # posts = cursor.fetchall()
   
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model= schemas.Post )
def create_posts(post : schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends
                 (oauth2.get_current_user)):
    
    
    new_post= models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #cursor.execute("""INSERT INTO posts (title, content , published) VALUES(%s, %s, %s) RETURNING * """,
                   #(post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit() #this works like save button in database GUI 
    
    return new_post


@router.get("/{id}",response_model= schemas.PostOut)
def get_posts(id : int,db: Session = Depends(get_db),user_id: int = Depends
                 (oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id= %s """, (str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
   
   
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"The details of id :  {id} is not found")
     
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id : int,db: Session = Depends(get_db),  current_user: int = Depends
                 (oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s returning * """, (str(id),)) #comma(,) fixing the error 
    # deleted_post = cursor.fetchone()
    # conn.commit() 
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"the posts you requested : {id} is not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform the requested action")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends
                 (oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s , content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post= cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"the posts you requested : {id} is not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"Not authorized to perform the requested action")
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    
    return post_query.first()


