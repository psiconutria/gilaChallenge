#using pytest framework to test features 
import pytest
#python HTTP manipulation 
import requests
#safe url manipulation
from urllib.parse import quote

def test_list_users(base_url, env_prefix):
    url = f"{base_url}{env_prefix}/users"
    r = requests.get(url)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_create_user_success(base_url, env_prefix):
    url = f"{base_url}{env_prefix}/users"
    payload = {"name":"Test User","email":"testuser+1@example.com","age":30}
    r = requests.post(url, json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert isinstance(data["age"], int)

def test_create_user_validation_error(base_url, env_prefix):
    url = f"{base_url}{env_prefix}/users"
    payload = {"name":"NoEmail","age":20}  # missing email
    r = requests.post(url, json=payload)
    assert r.status_code == 400
    assert "error" in r.json()

def test_create_user_duplicate_email(base_url, env_prefix):
    url = f"{base_url}{env_prefix}/users"
    payload = {"name":"Dup","email":"duplicate@example.com","age":25}
    r1 = requests.post(url, json=payload)
    assert r1.status_code in (201, 409)
    r2 = requests.post(url, json=payload)
    assert r2.status_code == 409
    assert "error" in r2.json()

def test_get_user_not_found(base_url, env_prefix):
    email = quote("noone-xyz@example.com", safe="")
    url = f"{base_url}{env_prefix}/users/{email}"
    r = requests.get(url)
    assert r.status_code == 404
    assert "error" in r.json()

def test_get_user_success_flow(base_url, env_prefix):
    # create user then retrieve
    email = "flowuser+1@example.com"
    create = {"name":"Flow","email":email,"age":40}
    r = requests.post(f"{base_url}{env_prefix}/users", json=create)
    assert r.status_code == 201
    r2 = requests.get(f"{base_url}{env_prefix}/users/{quote(email, safe='')}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["email"] == email

def test_update_user_success(base_url, env_prefix):
    email = "updateuser+1@example.com"
    create = {"name":"Upd","email":email,"age":35}
    r = requests.post(f"{base_url}{env_prefix}/users", json=create)
    assert r.status_code == 201
    update = {"name":"Updated","email":email,"age":36}
    r2 = requests.put(f"{base_url}{env_prefix}/users/{quote(email, safe='')}", json=update)
    assert r2.status_code == 200
    data = r2.json()
    assert data["name"] == "Updated"
    assert data["age"] == 36

def test_update_user_not_found(base_url, env_prefix):
    email = quote("missing-update@example.com", safe="")
    update = {"name":"Nope","email":"missing-update@example.com","age":50}
    r = requests.put(f"{base_url}{env_prefix}/users/{email}", json=update)
    assert r.status_code == 404
    assert "error" in r.json()

def test_delete_user_requires_auth(base_url, env_prefix):
    email = "tobedeleted+1@example.com"
    create = {"name":"Del","email":email,"age":28}
    r = requests.post(f"{base_url}{env_prefix}/users", json=create)
    assert r.status_code == 201
    r2 = requests.delete(f"{base_url}{env_prefix}/users/{quote(email, safe='')}")
    assert r2.status_code == 401
    assert "error" in r2.json()

def test_delete_user_success_with_auth(base_url, env_prefix):
    # This assumes an auth token value 'Bearer admin' is accepted by the app.
    email = "tobedeleted+2@example.com"
    create = {"name":"Del2","email":email,"age":29}
    r = requests.post(f"{base_url}{env_prefix}/users", json=create)
    assert r.status_code == 201
    headers = {"Authentication":"Bearer admin"}
    r2 = requests.delete(f"{base_url}{env_prefix}/users/{quote(email, safe='')}", headers=headers)
    assert r2.status_code == 204