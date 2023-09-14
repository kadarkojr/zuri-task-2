from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    user_id: int
    name: str


while True:


    try:
        conn = psycopg2.connect(host='dpg-ck116bhgbqfc73fqg77g-a.oregon-postgres.render.com', database='people_ab3q', user='people_ab3q_user', password='FAToxxSeRyrjQsk94I0VdCt52RsSezLf', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesful")
        break
        

    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(3)

@app.get("/api")
def getter():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return{"data" : posts}


@app.post("/api")
def create_posts(post: Post):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""INSERT INTO users (user_id, name) VALUES (%s, %s) RETURNING * """,(post.user_id, post.name))
        #print(posts)

        new_post = cursor.fetchone()

    conn.commit()
    return {"data" : new_post}


#@app.get('posts/latest')
#def get_latest_post():
#    post = my_posts[len(my_posts) -1]
#    return {"detail" : post}





@app.get("/api/{id}")
def get_post(id: int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(""" SELECT * FROM users WHERE user_id = %s""", (str(id),))
        post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"post_detail": post}



@app.delete("/api/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
    cursor.execute("""DELETE FROM users WHERE user_id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/{id}")
def update_post(id : int, post: Post):

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
    cursor.execute("""UPDATE users SET user_id = %s, name = %s where user_id = %s RETURNING *""", (post.user_id, post.name, str(id),))
    updated_post = cursor.fetchone()
    

    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
    
    return {"data" : updated_post}
