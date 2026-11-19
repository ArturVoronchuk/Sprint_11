import pytest
import requests

from helpers.listing_helper import create_listing
from helpers.user_generator import generate_user_payload
from urls import URL, USER_CREATE_ENDPOINT

@pytest.fixture
def registered_user():
    payload = generate_user_payload()
    response = requests.post(
        f"{URL}{USER_CREATE_ENDPOINT}", json=payload
    )
    return {
        "payload": payload,
        "id": response.json()["user"]["id"],
        "token": response.json()["access_token"]["access_token"],
    }

@pytest.fixture
def created_listing(registered_user):
    response = create_listing(registered_user["token"])
    assert response.status_code == 201, (
        f"Не удалось создать объявление в фикстуре. "
        f"Статус: {response.status_code}, ответ: {response.text}"
    )
    listing = response.json()
    return {"id": listing["id"], "data": listing, "user": registered_user}
