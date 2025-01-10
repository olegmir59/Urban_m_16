from fastapi import FastAPI, Path
from typing import Annotated

# Создаем экземпляр приложения FastAPI
app = FastAPI()
# Определение базового маршрута
@app.get("/")
async def get_root_page() -> dict:
    return {"message": "Главная страница"}


@app.get("/user/admin")
async def get_admin_page():
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def get_user_id(
        user_id: Annotated[int, Path(gt=0, le=100, description="Введите идентификатор пользователя", examples=1)]
) -> dict:
    return {"message": f"Вошли как пользователь № {user_id}"}


@app.get("/user/{username}/{age}")
async def get_user_info(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Введите имя пользователя", examples="UrbanUser")],
    age: Annotated[int, Path(ge=18, le=120, description="Введите возраст", examples=24)],
) -> dict:
    return {
        "message": f"Информация о пользователе. Имя: {username}, Возраст: {age}."
    }