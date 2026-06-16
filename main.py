from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import logging

# 1. إعداد نظام المراقبة الأمني
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. إعداد التطبيق
app = FastAPI(
    title="Secure User Management API",
    description="مشروع أمن سيبراني متقدم لإدارة بيانات المستخدمين مع حماية ضد BOLA",
    version="1.1.0"
)

# 3. تنظيم هيكلية البيانات
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

# قاعدة بيانات وهمية
db = {
    1: {"name": "أحمد", "email": "ahmed@example.com"},
    2: {"name": "سارة", "email": "sara@example.com"}
}

# 4. مسار الجذر
@app.get("/", tags=["General"])
def read_root():
    return {"message": "نظام الـ API يعمل بنجاح. اذهب إلى /docs لرؤية واجهة التوثيق."}

# 5. المسار المستهدف (مع تطبيق الحماية ضد ثغرة BOLA)
@app.get("/api/user/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int, x_user_id: int = Header(...)):
    """
    جلب بيانات المستخدم مع التحقق من الصلاحية (BOLA Protection)
    """
    # نفترض أن المستخدم الحالي الموثق لديه ID رقم 1
    CURRENT_AUTHENTICATED_USER = 1 
    
    # --- طبقة الحماية (Defense Layer) ---
    # نتحقق: هل الـ user_id الذي طلبه المهاجم يطابق هوية صاحب الطلب الفعلي؟
    if user_id != x_user_id:
        # تسجيل محاولة الاختراق في السجلات
        logger.warning(f"SECURITY ALERT: محاولة وصول غير مصرح بها! المستخدم {x_user_id} حاول الوصول للمستخدم {user_id}")
        
        # رفض الطلب بـ 403 Forbidden
        raise HTTPException(
            status_code=403, 
            detail="Forbidden: You do not have permission to access this user's data."
        )
    
    # التحقق من وجود المستخدم في القاعدة
    if user_id not in db:
        logger.error(f"محاولة وصول فاشلة لمستخدم غير موجود {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    logger.info(f"تم بنجاح الوصول إلى بيانات المستخدم رقم {user_id}")
    return {"id": user_id, **db[user_id]}
