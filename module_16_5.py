from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    age: int

users: List[User] = []

# Функция для генерации следующего id
def next_id() -> int:
    if len(users) == 0:
        return 1
    return users[-1].id + 1

# GET /users
@app.get('/users', response_model=List[User])
def get_users():
    return users

# POST /user/{username}/{age}
@app.post('/user/{username}/{age}', response_model=User)
def create_user(username: str, age: int):
    new_user = User(id=next_id(), username=username, age=age)
    users.append(new_user)
    return new_user

# PUT /user/{user_id}/{username}/{age}
@app.put('/user/{user_id}/{username}/{age}', response_model=User)
def update_user(user_id: int, username: str, age: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i] = User(id=user_id, username=username, age=age)
            return users[i]
    raise HTTPException(status_code=404, detail="User was not found")

# DELETE /user/{user_id}
@app.delete('/user/{user_id}', response_model=Optional[User])
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            removed_user = users.pop(i)
            return removed_user
    raise HTTPException(status_code=404, detail="User was not found")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
