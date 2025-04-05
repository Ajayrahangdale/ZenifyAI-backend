from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(name="Ajay", age=25)
print(user)
