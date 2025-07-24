from app import schemas
from .database import client, session
import pytest
from jose import jwt


from app.config import settings

import pytest

def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "Hello World! On 1 September 2025, a new life starts. I mean it"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "fuck_julia@gmail.com", "password": "123"})

    new_user = schemas.UserInfo(**res.json())
    assert new_user.email == "fuck_julia@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    # not JSON form, but data form
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'