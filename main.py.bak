from fastapi import FastAPI
app = FastAPI()

# محاكاة قاعدة بيانات للمستخدمين
users = {
    1: {"name": "أحمد", "secret": "كلمة سر أحمد هي 123"},
    2: {"name": "سارة", "secret": "كلمة سر سارة هي abc"}
}

@app.get("/api/user/{user_id}")
def get_user(user_id: int):
    # الثغرة: لا يوجد تحقق من هوية المستخدم الذي يطلب البيانات
    return users.get(user_id, {"error": "User not found"})
