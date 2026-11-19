import allure
import requests

from data import EXISTING_USER_MESSAGE
from helpers.user_generator import generate_user_payload
from urls import URL, USER_CREATE_ENDPOINT

@allure.feature("API создания пользователя")
class TestUserCreating:

    @allure.title(
        "Проверяем, что новый пользователь успешно создается. "
        "Запрос возвращает: "
        "статус код 201 и id пользователя"
    )
    def test_new_user_is_successfully_created(self):

        payload = generate_user_payload()

        with allure.step("Создаем нового пользователя"):
            response = requests.post(
                f"{URL}{USER_CREATE_ENDPOINT}", json=payload
            )

        with allure.step(
                "Проверяем, что при успешной попытке создать нового пользователя возвращается статус код - 201"
        ):
            assert response.status_code == 201, (
                f"Ожидался статус код 201, но получен {response.status_code}. Ответ: {response.text}"
            )

        body = response.json()

        with allure.step(
                "Проверяем, что в ответе есть id пользователя и оно не пустое"
        ):
            assert body["user"]["id"], \
                "В ответе отсутствует id пользователя"

        with allure.step(
                "Проверяем, что в теле запроса возвращается тот же email, что был передан в запросе"
        ):
            assert body["user"]["email"] == payload["email"], (
                "Email в ответе не совпадает с отправленным"
            )

        with allure.step("Проверяем, что в ответе есть непустой access_token"):
            assert body["access_token"]["access_token"], \
                "В ответе отсутствует access_token"

    @allure.title(
        "Проверяем, что повторная регистрация пользователя возвращает "
        "статус код 400 и message описанием ошибки"
    )
    def test_attempt_create_existing_user_returns_error(self, registered_user):

        with allure.step("Повторно регистрируем пользователя с уже существующим email"):
            duplicate_response = requests.post(
                f"{URL}{USER_CREATE_ENDPOINT}",
                json=registered_user["payload"]
            )

        with allure.step(
                "Проверяем, что при повторной регистрации возвращается статус код - 400"
        ):
            assert duplicate_response.status_code == 400, (
                f"Ожидался статус код 400, но получен {duplicate_response.status_code}. "
                f"Ответ: {duplicate_response.text}"
            )

        body = duplicate_response.json()

        with allure.step(f"Проверяем, что вернулся текст ошибки - {EXISTING_USER_MESSAGE}"):
            assert body["message"] == EXISTING_USER_MESSAGE, \
                f"Текст ошибки не совпадает с {EXISTING_USER_MESSAGE}"