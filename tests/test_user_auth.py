import allure
import requests

from urls import URL, USER_AUTH_ENDPOINT

@allure.feature("API авторизации пользователя")
class TestUserAuth:

    def test_successful_user_auth_return_status_code_201(self, registered_user):

        with allure.step("Авторизуемся под созданным пользователем"):
            response = requests.post(
                f"{URL}{USER_AUTH_ENDPOINT}",
                json=registered_user["payload"])

        with allure.step(
                "Проверяем, что при успешной авторизации "
                "пользователя возвращается статус код - 201"
        ):
            assert response.status_code == 201, (
                f"Ожидался статус код 201, но получен {response.status_code}. "
                f"Ответ: {response.text}"
            )

        body = response.json()

        with allure.step(
                "Проверяем, что при авторизации вернулся тот же пользователь, "
                "что был создан (id совпадает)"
        ):
            assert body["user"]["id"] == registered_user["id"], (
                f"id пользователя при авторизации ({body['user']['id']}) "
                f"не совпадает с id при регистрации ({registered_user['id']})"
            )

        with allure.step(
                "Проверяем, что в теле запроса возвращается тот же email, "
                "что был передан в запросе на авторизацию"
        ):
            assert body["user"]["email"] == registered_user["payload"]["email"], (
                "Email в ответе не совпадает с отправленным"
            )

        with allure.step("Проверяем, что в ответе есть непустой access_token"):
            assert body["token"]["access_token"], \
                "В ответе отсутствует access_token"