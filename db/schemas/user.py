from db.models.user import User

def user_schema(user) -> dict:
    return User(**{"id": str(user["_id"]),
              "username": user["username"],
              "email": user["email"]})
  
def users_schema(users) -> list:
    return [user_schema(user) for user in users]