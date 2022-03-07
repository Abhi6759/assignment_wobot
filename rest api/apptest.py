import json

import requests

access_token = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiaGlzaGVrQGdtYWlsLmNvbSJ9.wzDVAXYMtYaMoLqkRFJWXopIMGlXNREOQ8UUsNoEyp8"}

base_url = "http://127.0.0.1:8000/"

body = {
    "token": access_token['token'],
    "name": "nikhil",
    "age": "26",
    "city": "thane"
}


def test_access_token():
    body = {
        "email": "abhishek@gmail.com",
        "password": "abhishek"}
    response = requests.post(url=base_url + "login", data=json.dumps(body))
    token = json.loads(response.text)
    assert response.status_code == 200
    assert access_token['token'] == token['access_token']


# test to create a user with all valid data
def test_Create_user():
    response = requests.post(url=base_url + "users", data=json.dumps(body))
    assert response.status_code == 201


# test to get all users without parameters
def test_get_users1():
    response = requests.get(url=base_url + "users", data=json.dumps(access_token))
    assert response.status_code == 200


# test to get all users with filter of the city
def test_get_users2():
    response = requests.get(url=base_url + "users?city=thane", data=json.dumps(access_token))
    assert response.status_code == 200


#
# test to get all the users with the names matching the query
def test_get_users3():
    response = requests.get(url=base_url + "users?name=abhishek", data=json.dumps(access_token))
    assert response.status_code == 200


# test  to get all the users with invalid query
def test_get_users4():
    response = requests.get(url=base_url + "users?name=1263832", data=json.dumps(access_token))
    assert response.status_code == 404


# test  to get all the users without the accesstoken
def test_get_users5():
    response = requests.get(url=base_url + "users")
    assert response.status_code == 422


# test  to get all the users with wrong the access token
def test_get_users6():
    wrong_acess_token = {"token": "hbhvbefhjbdsiwbd"}
    response = requests.get(url=base_url + "users", data=json.dumps(wrong_acess_token))
    assert response.status_code == 401


# test to get specific users
def test_get_specific_user1():
    response = requests.get(url=base_url + "users/1", data=json.dumps(access_token))
    assert response.status_code == 200


# test to get user which doesnt exist
def test_get_specific_user2():
    response = requests.get(url=base_url + "users/999999", data=json.dumps(access_token))
    assert response.status_code == 404


# test to get a user by giving wrong query
def test_get_specific_user3():
    response = requests.get(url=base_url + "users/abhishek", data=json.dumps(access_token))
    assert response.status_code == 422


# test to delete the user
# def test_delete_specific_user1():
#     response = requests.delete(url=base_url + "users/4", data=json.dumps(access_token))
#     assert response.status_code == 204


# test to update user info
def update_user1():
    response = requests.post(url=base_url + "users/3", data=json.dumps(body))
    assert response.status_code == 202


# test to update the user info with doesnt exist
def update_user2():
    response = requests.post(url=base_url + "users/22233", data=json.dumps(body))
    assert response.status_code == 404


# test to update a user with invalid query
def update_user3():
    response = requests.post(url=base_url + "users/sacu", data=json.dumps(body))
    assert response.status_code == 422
