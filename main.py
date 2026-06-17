from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# قاعدة بيانات وهمية
db = {
    1: {"name": "أحمد", "email": "ahmed@example.com"},
    2: {"name": "سارة", "email": "sara@example.com"}
}

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/api/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    # الثغرة تكمن هنا: السيرفر يثق في الـ ID القادم من الرابط فوراً
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}
