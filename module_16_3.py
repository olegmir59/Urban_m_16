from fastapi import FastAPI, Path, Request, Response
import uvicorn

app = FastAPI()

# Словарь для хранения пользователей
users = {'1': 'Имя: Example, возраст: 18'}

# Функция для генерации следующего ключа
def next_key():
    keys = list(map(int, users.keys()))
    if not keys:
        return '1'
    return str(max(keys) + 1)

# GET /users
@app.get('/users')
def get_users():
    return users

# POST /user/{username}/{age}
@app.post('/user/{username}/{age}')
def create_user(
    username: str, age: int):
    user_id = next_key()
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} is registered'

# PUT /user/{user_id}/{username}/{age}
@app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: str, username: str, age: int):
    if user_id in users:
        users[user_id] = f'Имя: {username}, возраст: {age}'
        return f'The user {user_id} is updated'
    return Response(status_code=404, content=f'User with id {user_id} does not exist')

# DELETE /user/{user_id}
@app.delete('/user/{user_id}')
def delete_user(user_id: str):
    if user_id in users:
        del users[user_id]
        return f'User {user_id} has been deleted'
    return Response(status_code=404, content=f'User with id {user_id} does not exist')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)