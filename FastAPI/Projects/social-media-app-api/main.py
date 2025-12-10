from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"id": 1, "title": "This is post 1", "Content": "This is content of post 1"}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found with the id {id}")
        # to writing this we have another way given above of HTTPException
        # response.status_code = status.HTTP_404_NOT_FOUND #404
        # return{"mesage": "Not found"}
    return {"post": post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
#* payload/body anything need to send data in our post request. the Body is from fastapi.param and we declare a variabel name as payload/body which is of dictionary type and anything we pass in our request body for post method will be stored there.
def create_post(post: Post):  #?payload: dict = Body(...)
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {'post': post_dict}
    # print(post.rating )
    #! for converting our pydantic model into dictionary
    # print(post.dict()) 
    # return {"message": "Post created successfully"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    # * Delete Post
    # * Find index of Post that has required ID
    # * Post.pop
    post_index = find_post_index(id)
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {id} is not exists")
    my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/post/{id}")
def update_post(id: int, post: Post):
    print(post)
    return{'mesase': 'updated data'}