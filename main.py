from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# 1. إعداد نظام المراقبة (Security Logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. إعداد التطبيق مع العنوان الذي سيظهر في Swagger UI
app = FastAPI(
    title="Secure User Management API",
    description="مشروع أمن سيبراني متقدم لإدارة بيانات المستخدمين",
    version="1.0.0"
)

# 3. استخدام Pydantic Models لتنظيم البيانات (هيكلية احترافية)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

# محاكاة قاعدة بيانات
db = {
    1: {"name": "أحمد", "email": "ahmed@example.com"},
    2: {"name": "سارة", "email": "sara@example.com"}
}

# 4. مسار الجذر (لحل مشكلة الصفحة البائسة)
@app.get("/", tags=["General"])
def read_root():
    return {"message": "نظام الـ API يعمل بنجاح. اذهب إلى /docs لرؤية واجهة التوثيق."}

# 5. المسار المستهدف (مع Logging للعمليات)
@app.get("/api/user/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int):
    if user_id not in db:
        logger.error(f"محاولة وصول فاشلة للمستخدم رقم {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"تم بنجاح الوصول إلى بيانات المستخدم رقم {user_id}")
    return {"id": user_id, **db[user_id]}
