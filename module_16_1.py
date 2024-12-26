from fastapi import FastAPI
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
async def get_user_id(user_id: int) -> dict:
    return {"message": f"Вошли как пользователь № {user_id}"}

@app.get("/user/")
async def get_user_info(user_id=None) -> dict:
    if user_id is None:
        return {"message": "Информация о пользователе. Имя: <username>, Возраст: <age>."}
    else:
        # Здесь мог бы быть дополнительный код для обработки ситуации,
        # когда `user_id` передан, но он отсутствует в базе.
        return {"message": f"Информация о пользователе. Имя: <username>, Возраст: <age>."}
