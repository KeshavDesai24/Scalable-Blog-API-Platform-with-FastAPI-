import pytest
from jose import jwt
from app import schemas
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == 'Hello Developers'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users", json={"email": "testing123@gmail.com", "password": "testing123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "testing123@gmail.com"
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
 
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('keshav@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('keshav@gmail.com', None, 422)
])   
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == 403
    #assert res.json().get('detail') == 'Invalid Credentials'