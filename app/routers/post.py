
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts", tags=["Posts"]
    )


# getting one post 
@router.get("/{id}", response_model = schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # make sure that id is a int. If str, error 
    
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
    # #cursor.execute(f"SELECT * FROM posts WHERE id = {id}") -> SQL injection
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
    return post


#getting all posts
@router.get("/", response_model = List[schemas.PostOut])
#@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall() 
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(
            limit).offset(skip).all()
    return posts
    #return [{"post": post, "votes": vote_count} for post, vote_count in results]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #vulnerable for SQL injection 
    #cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})")
    # not vulnerable for SQL injection 
    
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)

    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # similarly to postgree commmit
    db.add(new_post)
    db.commit()
    # to return just added post
    db.refresh(new_post)
    return new_post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #OMR code

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} does not exist in our database")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    
    # post_query.update({"title" : "Sorry", "content": "Julia, sorry, I would fuck you! always! sorry for the black-haired girl"}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()