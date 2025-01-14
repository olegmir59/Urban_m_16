from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, Dict, Any
import uvicorn

app = FastAPI()

# Словарь для хранения пользователей
users: Dict[str, str] = {'1': 'Имя: Example, возраст: 18'}


# Функция для генерации следующего ключа
def next_key() -> str:
    keys = list(map(int, users.keys()))
    if not keys:
        return '1'
    return str(max(keys) + 1)


# GET /users
@app.get('/users')
def get_users() -> Dict[str, str]:
    return users


# POST /user/{username}/{age}
@app.post('/user/{username}/{age}')
def create_user(
        username: Annotated[
            str, Path(min_length=5, max_length=50, description="Введите имя пользователя", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Введите возраст", example=24)]
) -> str:
    user_id = next_key()
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} is registered'


# PUT /user/{user_id}/{username}/{age}
@app.put('/user/{user_id}/{username}/{age}')
def update_user(
        user_id: Annotated[str, Path(description="Введите идентификатор пользователя", example="1")],
        username: Annotated[
            str, Path(min_length=5, max_length=50, description="Введите имя пользователя", example="UrbanUser")],
        age: Annotated[int, Path(ge=18, le=120, description="Введите возраст", example=24)]
) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f'Пользователь с id {user_id} не найден')

    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'Пользователь {user_id} был обновлен'


# DELETE /user/{user_id}
@app.delete('/user/{user_id}')
def delete_user(
        user_id: Annotated[str, Path(description="Введите идентификатор пользователя", example="1")]
) -> str:
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f'Пользователь с id {user_id} не найден')

    del users[user_id]
    return f'Пользователь {user_id} был удален'

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
