from helpers.user_generator import UserGenerator

EXISTING_USER_MESSAGE  = "Почта уже используется"

def generate_listing_data():
    return {
        "category": "Книги",
        "city": "Нижний Новгород",
        "condition": "Новый",
        "description": UserGenerator.random_string(),
        "name": UserGenerator.random_string(),
        "price": "1111",
    }

UPDATE_OFFER_FORBIDDEN = "Оффер не найден или у вас нет прав на его редактирование"
DELETE_OFFER_COMPLETE = "Объявление удалено успешно"