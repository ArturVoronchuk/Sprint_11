import allure
import requests

from data import generate_listing_data, UPDATE_OFFER_FORBIDDEN, DELETE_OFFER_COMPLETE
from helpers.listing_helper import create_listing, update_listing, delete_listing
from helpers.user_generator import UserGenerator, generate_user_payload
from urls import URL, USER_CREATE_ENDPOINT


@allure.feature("API создания/изменения/удаления объявлений")
class TestAdvertisement:

    @allure.title(
        "Проверяем, что создание объявления возвращает статус код 201 и "
        "все поля в ответе на запрос соответствуют тем, что были переданы"
    )
    def test_successful_creation_new_ad_returns_status_code_201(self, registered_user):
        listing_data = generate_listing_data()

        with allure.step("Создаём объявление"):
            response = create_listing(registered_user["token"], listing_data)

        with allure.step("Проверяем статус код 201"):
            assert response.status_code == 201, \
                f"Ожидался 201, получен {response.status_code}. Ответ: {response.text}"

        body = response.json()

        with allure.step("Проверяем, что поля объявления совпадают с отправленными"):
            assert body["name"] == listing_data["name"]
            assert body["category"] == listing_data["category"]
            assert body["condition"] == listing_data["condition"]
            assert body["city"] == listing_data["city"]
            assert body["description"] == listing_data["description"]
            assert body["price"] == int(listing_data["price"])

        with allure.step("Проверяем, что владелец — авторизованный пользователь"):
            assert body["owner"] == registered_user["id"], \
            "Поля id и owner не совпадают"

    @allure.title("Проверяем, что авторизованный пользователь успешно редактирует своё объявление")
    def test_successful_edit_listing(self, created_listing):
        new_name = UserGenerator.random_string()
        new_description = UserGenerator.random_string()

        listing_data = {
            "category": created_listing["data"]["category"],
            "condition": created_listing["data"]["condition"],
            "city": created_listing["data"]["city"],
            "description": new_description,
            "name": new_name,
            "price": str(created_listing["data"]["price"]),
        }

        with allure.step("Редактируем поля name и description объявления"):
            response = update_listing(
                created_listing["id"],
                created_listing["user"]["token"],
                listing_data,
            )

        with allure.step("Проверяем, что возвращается статус код 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"

        body = response.json()

        with allure.step("Проверяем, что поля name и description изменились"):
            assert body["name"] == new_name, "Название объявления не изменилось"
            assert body["description"] == new_description, "Описание объявления не изменилось"

        with allure.step("Проверяем, что остальные поля не изменились"):
            assert body["category"] == listing_data["category"]
            assert body["condition"] == listing_data["condition"]
            assert body["city"] == listing_data["city"]
            assert body["price"] == int(listing_data["price"])

    @allure.title("Проверяем, что пользователь не может редактировать чужое объявление")
    def test_edit_foreign_listing_is_forbidden(self, created_listing):

        with allure.step("Создаем второго пользователя"):
            second_payload = generate_user_payload()
            second_response = requests.post(
                f"{URL}{USER_CREATE_ENDPOINT}", json=second_payload
            )
            assert second_response.status_code == 201, (
                f"Не удалось создать второго пользователя. "
                f"Статус: {second_response.status_code}, ответ: {second_response.text}"
            )

        second_token = second_response.json()["access_token"]["access_token"]

        listing_data = {
            "category": created_listing["data"]["category"],
            "condition": created_listing["data"]["condition"],
            "city": created_listing["data"]["city"],
            "description": UserGenerator.random_string(),
            "name": UserGenerator.random_string(),
            "price": str(created_listing["data"]["price"]),
        }

        with allure.step("Пытаемся отредактировать чужое объявление под токеном второго пользователя"):
            response = update_listing(
                created_listing["id"],
                second_token,
                listing_data,
            )

        with allure.step(
                "Проверяем, что сервер запрещает редактирование чужого объявления "
                "и возвращает статус код 401"
        ):
            assert response.status_code == 401, \
                f"Ожидался 401, получен {response.status_code}. Ответ: {response.text}"

        data = response.json()

        with allure.step(f"Проверяем, что сообщение в ответе соответствует {UPDATE_OFFER_FORBIDDEN}"):
            assert data["message"] == UPDATE_OFFER_FORBIDDEN, \
                f"Поле 'message' не {UPDATE_OFFER_FORBIDDEN}"

    @allure.title("Проверяем, что авторизованный пользователь успешно удаляет своё объявление")
    def test_successful_delete_listing(self, created_listing):
        with allure.step("Удаляем объявление"):
            response = delete_listing(
                created_listing["id"],
                created_listing["user"]["token"],
            )

        with allure.step("Проверяем, что возвращается статус код 200"):
            assert response.status_code == 200, (
                f"Ожидался 200, получен {response.status_code}. Ответ: {response.text}"
            )

        data = response.json()

        with allure.step(f"Проверяем, что сообщение в ответе соответствует {DELETE_OFFER_COMPLETE}"):
            assert data["message"] == DELETE_OFFER_COMPLETE, \
                f"Поле 'message' не {DELETE_OFFER_COMPLETE}"