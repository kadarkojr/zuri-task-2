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
    name: str


while True:


    try:
        conn = psycopg2.connect(host='dpg-ck1ptp821fec738hdjo0-a.oregon-postgres.render.com', database='myusers', user='myusers_user', password='oWsU8128G94ZZUgz8itB8qriiiVjgJe4', cursor_factory=RealDictCursor)
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
    # Check if a record with the same name already exists
        cursor.execute("SELECT id FROM users WHERE name = %s", (post.name,))
        existing_record = cursor.fetchone()

        if existing_record:
        # If a record with the same name exists, raise an exception
            raise HTTPException(status_code=400, detail="Name Already Registered")

    # If no record with the same name exists, insert the new record
        cursor.execute("INSERT INTO users (name) VALUES (%s) RETURNING *", (post.name,))
        new_post = cursor.fetchone()

    conn.commit()
    return {"data": new_post}



#@app.get('posts/latest')
#def get_latest_post():
#    post = my_posts[len(my_posts) -1]
#    return {"detail" : post}





@app.get("/api/{id}")
def get_post(id : int):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(""" SELECT * FROM users WHERE id = %s""", (str(id),))
        post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"data" : f"post with id {id} was not found"}
    return {"post_detail" : post}


@app.delete("/api/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""DELETE FROM users WHERE id = %s returning *""", (str(id),))
        deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/{id}")
def update_post(id: int, post: Post):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        # Check if the record with the specified ID exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (id,))
        existing_record = cursor.fetchone()

        if existing_record is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

        # Update the record with the specified ID
        cursor.execute("UPDATE users SET name = %s WHERE id = %s RETURNING *", (post.name, id))
        updated_post = cursor.fetchone()

    conn.commit()
    
    return {"data": updated_post}
