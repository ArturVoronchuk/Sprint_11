import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from data import generate_listing_data
from urls import URL, CREATE_LISTING_ENDPOINT, UPDATE_LISTING_ENDPOINT, DELETE_LISTING_ENDPOINT


def create_listing(token, listing_data=None):
    fields = listing_data or generate_listing_data()
    multipart_data = MultipartEncoder(fields=fields)
    return requests.post(
        f"{URL}{CREATE_LISTING_ENDPOINT}",
        data=multipart_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": multipart_data.content_type,
        },
    )

def update_listing(listing_id, token, fields):
    multipart_data = MultipartEncoder(fields=fields)
    return requests.patch(
        f"{URL}{UPDATE_LISTING_ENDPOINT.format(listing_id=listing_id)}",
        data=multipart_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": multipart_data.content_type,
        },
    )

def delete_listing(listing_id, token):
    return requests.delete(
        f"{URL}{DELETE_LISTING_ENDPOINT.format(listing_id=listing_id)}",
        headers={"Authorization": f"Bearer {token}"}
    )