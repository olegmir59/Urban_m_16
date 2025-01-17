from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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

# GET /
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

'''
# GET /users
@app.get('/users', response_model=List[User])
def get_users():
    return users
'''

# GET /user/{user_id}
@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user_by_id(request: Request, user_id: int):
    try:
        user = next(u for u in users if u.id == user_id)
        return templates.TemplateResponse("users.html", {"request": request, "user": user})
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")

# POST /user/{username}/{age}
@app.post('/user/{username}/{age}', response_model=User)
def create_user(username: str, age: int):
    new_user = User(id=next_id(), username=username, age=age)
    users.append(new_user)
    return RedirectResponse(url="/", status_code=303)

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
