import requests

BASE_URL = "http://127.0.0.1:5000/api"

login_data = {"username": "test", "password": "test"}
response = requests.post(f"{BASE_URL}/login", json=login_data)

print("Login Status Code:", response.status_code)
print("Login Response Text:", response.text)

try:
    token = response.json().get("access_token")
    if not token:
        print("Error: No access token received!")
        exit()
except requests.exceptions.JSONDecodeError:
    print("Error: Login response is not valid JSON!")
    exit()

headers = {"Authorization": f"Bearer {token}"}

movies_response = requests.get(f"{BASE_URL}/movies", headers=headers)
print("Movies Status Code:", movies_response.status_code)
print("Movies:", movies_response.json() if movies_response.ok else movies_response.text)

new_movie = {
    "name": "Interstellar",
    "year": 2014,
    "awards": 5,
    "genre": "Sci-Fi"
}
add_response = requests.post(f"{BASE_URL}/movies", json=new_movie, headers=headers)
print("Add Movie Status Code:", add_response.status_code)
print("Add Movie:", add_response.json() if add_response.ok else add_response.text)

movie_id = 1 
movie_details = requests.get(f"{BASE_URL}/movies/{movie_id}", headers=headers)
print("Movie Details Status Code:", movie_details.status_code)
print("Movie Details:", movie_details.json() if movie_details.ok else movie_details.text)

update_data = {"name": "Interstellar (Updated)", "genre": "Sci-Fi/Adventure"}
update_response = requests.put(f"{BASE_URL}/movies/{movie_id}", json=update_data, headers=headers)
print("Update Movie Status Code:", update_response.status_code)
print("Update Movie:", update_response.json() if update_response.ok else update_response.text)

delete_response = requests.delete(f"{BASE_URL}/movies/{movie_id}", headers=headers)
print("Delete Movie Status Code:", delete_response.status_code)
print("Delete Movie:", delete_response.json() if delete_response.ok else delete_response.text)
