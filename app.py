from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

app = FastAPI()

def load_mock_data():
    with open('mock_data.json') as f:
        return json.load(f)

def save_mock_data(data):
    with open('mock_data.json', 'w') as f:
        json.dump(data, f, indent=4)

class User(BaseModel):
    name: str
    email: str

@app.get("/users")
def get_users():
    data = load_mock_data()
    return JSONResponse(content=data)

@app.get("/users/{id}")
def get_user_by_id(id: int):
    data = load_mock_data()
    users = data["users"]
    user = next((user for user in users if user["id"] == id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"user": user})

@app.post("/users")
def create_user(user: User):
    data = load_mock_data()
    users = data["users"]
    new_id = max([u["id"] for u in users], default=0) + 1
    new_user = {"id": new_id, "name": user.name, "email": user.email}
    users.append(new_user)
    data["users"] = users
    save_mock_data(data)
    return JSONResponse(content={"user": new_user}, status_code=201)

@app.put("/users/{id}")
def update_user(id: int, user: User):
    data = load_mock_data()
    users = data["users"]
    existing_user = next((u for u in users if u["id"] == id), None)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user["name"] = user.name
    existing_user["email"] = user.email
    save_mock_data(data)
    return JSONResponse(content={"user": existing_user})

@app.delete("/users/{id}")
def delete_user(id: int):
    data = load_mock_data()
    users = data["users"]
    user_to_delete = next((user for user in users if user["id"] == id), None)
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove the user from the list
    users = [user for user in users if user["id"] != id]
    data["users"] = users
    save_mock_data(data)
    
    return JSONResponse(content={"message": f"User with id {id} has been deleted"}, status_code=200)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Test API"}
