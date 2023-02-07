import uuid
import time
import json
import django.utils.timezone as timezone
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from puyen.settings import EMAIL_HOST_USER
from user.mod import getRandom
from user.models import User_account, User_set, User_default, User_put, User_a1c, User_Weight, User_Pressure, User_Sugar, User_diet, User_medical, User_friend_request, User_friend, Care_message, User_drug

# Create your views here.


@ csrf_exempt  # 1. 註冊 W
def register(request):
    if request.method == "POST":
        try:
            # 取得及產生註冊資料
            data = json.loads(request.body)
            id = uuid.uuid4()
            now_time = timezone.now().isoformat(timespec="seconds")
            # 建立帳戶資料庫
            user_account = User_account.objects.create_user(
                username=data["account"], account=data["account"], email=data["email"], 
                id=id, friend_id=getRandom(), created_at=now_time, updated_at=now_time
            )
            user_account.set_password(data["password"])
            user_account.save()
            user = User_account.objects.get(id=id)
            User_set.objects.create(user=user, updated_at=now_time)
            User_default.objects.create(user=user, created_at=now_time)
            User_put.objects.create(user=user, created_at=now_time)
            User_medical.objects.create(user=user, created_at=now_time)
            return JsonResponse({"status": "0"})
        except Exception as e:
            return JsonResponse({"status": "1"})


@ csrf_exempt
def login(request):  # 2. 登入 W
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 帳號驗證檢查及回傳Token
            user = auth.authenticate(username=data['account'], password=data['password'])
            if user.account_ck == True:
                auth.login(request, user)
                request.session['id'] = user.id
                request.session.save()
                return JsonResponse({"status": "0", "token": request.session.session_key})   
            raise Exception
        except Exception as e:
            return JsonResponse({"status": "1" if user is None else "2"})


@ csrf_exempt
def send(request):  # 3. 發送驗證碼 W
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 產生驗證碼及發送
            send_mail(
                "使用者:{}您好，這是您的普元驗證信".format(data["email"]),
                "驗證碼:{}".format(getRandom()), 
                EMAIL_HOST_USER, [data["email"]]
            )
            return JsonResponse({"status": "0"})
        except Exception as e:
            return JsonResponse({"status": "1"})


@ csrf_exempt
def check(request):  # 4. 檢查驗證碼 (不會用到)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 帳號是存在及驗證
            user = User_account.objects.filter(mail_id=data["code"], phone=data["phone"])
            if not user.exists():
                raise Exception
            user.update(account_ck=True)
            return JsonResponse({"status": "0"})
        except Exception as e:
            return JsonResponse({"status": "1"})


@ csrf_exempt
def forgot(request):  # 5. 忘記密碼 W
    if request.method == "POST":
        try:
            user = User_set.objects.get(phone=request.body.decode().replace("email=&phone=", "")).user
            # 帳號存在判斷
            if user is None:
                raise Exception
            # 建立暫時密碼資料與寄信
            rand_password = getRandom()
            user.must_change_password = True
            send_mail(
                "使用者:{}您好，請重設密碼".format(user.email), 
                "暫時密碼為:{}，請重設盡速密碼。".format(rand_password), 
                EMAIL_HOST_USER, [user.email]
            )
            user.set_password(rand_password)
            user.save()
            return JsonResponse({"status": "0"})
        except Exception as e:
            return JsonResponse({"status": "1"})


@ csrf_exempt
def reset(request):  # 6. 重設密碼 W
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 建立重設密碼資料
            user = User_account.objects.get(
                id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            )
            user.set_password(data["password"])
            user.must_change_password = False
            user.save()
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def recheck(request):  # 38. 註冊確認  W
    if request.method == "GET":
        try:
            # 帳號存在判斷
            if User_account.objects.filter(account=request.GET["account"]).exists():
                 raise Exception
            return JsonResponse({"status": "0"})
        except Exception as e:
            return JsonResponse({"status": "1"})


@ csrf_exempt
def userset(request):  # 7. 個人資訊設定、12. 個人資訊 W
    try:
        user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
        if request.method == "PATCH":
            data = json.loads(request.body)
            # 更新個人資訊
            User_set.objects.filter(user=User_account.objects.get(id=user_id)
            ).update(
                name=data["name"], birthday=data["birthday"], 
                height=data["height"], gender=data["gender"], 
                address=data["address"], weight=data["weight"], 
                phone=data["phone"], email=data["email"], 
                updated_at=timezone.now().isoformat(timespec="seconds")
            )
            return JsonResponse({"status": "0"})
        if request.method == "GET":
            # 取得資料庫中個人資訊
            user_account = User_account.objects.get(id=user_id)
            user_set = User_set.objects.get(user=user_account)
            user_default = User_default.objects.get(user=user_account)
            user_setting = User_put.objects.get(user=user_account)
            user_data = {
                "id": user_id,
                "name": user_set.name,
                "account": user_account.account,
                "email": user_account.email,
                "phone": user_set.phone,
                "birthday": user_set.birthday,
                "height": user_set.height,
                "weight": float(user_set.weight),
                "gender": user_set.gender,
                "address": user_set.address,
                "default": {
                    "sugar_morning_max": user_default.sugar_morning_max, 
                    "sugar_morning_min": user_default.sugar_morning_min,
                    "sugar_evening_max": user_default.sugar_evening_max,
                    "sugar_evening_min": user_default.sugar_evening_min,
                    "sugar_before_max": user_default.sugar_before_max,
                    "sugar_before_min": user_default.sugar_before_min,
                    "sugar_after_max": user_default.sugar_after_max,
                    "sugar_after_min": user_default.sugar_after_min,
                    "systolic_max": user_default.systolic_max,
                    "systolic_min": user_default.systolic_min,
                    "diastolic_max": user_default.diastolic_max,
                    "diastolic_min": user_default.diastolic_min,
                    "pulse_max": user_default.pulse_max,
                    "pulse_min": user_default.pulse_min,
                    "weight_max": user_default.weight_max,
                    "weight_min": user_default.weight_min,
                    "body_fat_max": user_default.body_fat_max,
                    "body_fat_min": user_default.body_fat_min
                },
                "setting": {
                    "after_meal": user_setting.after_meal, 
                    "unit_of_height": user_setting.unit_of_height, 
                    "unit_of_sugar": user_setting.unit_of_sugar, 
                    "unit_of_weight": user_setting.unit_of_weight,
                    'over_max_or_under_min': user_setting.over_max_or_under_min, 
                    'no_recording_for_a_day': user_setting.no_recording_for_a_day, 
                    'after_recording': user_setting.after_recording
                }
            }
            return JsonResponse({"status": "0", "user": user_data})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def default(request):  # 11. 個人預設值 
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            user_id = User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"])
            now_time = timezone.now().isoformat(timespec="seconds")
            # 路徑判斷以及更新個人預設值
            # setatter函數
            if data.setdefault("sugar_morning_max", "Null") != "Null":
                User_default.objects.update(
                    user=user_id, updated_at=now_time,
                    sugar_morning_max=data["sugar_morning_max"], sugar_morning_min=data["sugar_morning_min"], 
                    sugar_evening_max=data["sugar_evening_max"], sugar_evening_min=data["sugar_evening_min"], 
                    sugar_before_max=data["sugar_before_max"], sugar_before_min=data["sugar_before_min"], 
                    sugar_after_max=data["sugar_after_max"], sugar_after_min=data["sugar_after_min"] 
                )
            elif data.setdefault("systolic_max", "Null") != "Null":
                 User_default.objects.update(
                    user=user_id, updated_at=now_time,
                    systolic_max=data["systolic_max"], systolic_min=data["systolic_min"], 
                    diastolic_max=data["diastolic_max"], diastolic_min=data["diastolic_min"], 
                    pulse_max=data["pulse_max"], pulse_min=data["pulse_min"]
                 )
            elif data.setdefault("weight_max", "Null") != "Null":
                User_default.objects.update(
                    user=user_id, updated_at=now_time,
                    weight_max=data["weight_max"], weight_min=data["weight_min"]
                 )
            elif data.setdefault("body_fat_max", "Null") != "Null":
                User_default.objects.update(
                    user=user_id, updated_at=now_time,
                    body_fat_max=data["body_fat_max"], body_fat_min=data["body_fat_min"]
                 )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def setting(request):  # 35. 個人設定 
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            # 個人設定更新
            user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            now_time = timezone.now().isoformat(timespec="seconds")
            if data.setdefault("over_max_or_under_min", "Null") != "Null":
                User_put.objects.update(
                user=User_account.objects.get(id=user_id), over_max_or_under_min=data["over_max_or_under_min"], 
                after_recording=data["after_recording"], no_recording_for_a_day=data["no_recording_for_a_day"],  
                updated_at=now_time
            ) 
            else:
                User_put.objects.update(
                    user=User_account.objects.get(id=user_id), after_meal=data["after_meal"], 
                    unit_of_sugar=data["unit_of_sugar"], unit_of_weight=data["unit_of_weight"], 
                    unit_of_height=data["unit_of_height"], updated_at=now_time
                )      
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def pressure(request):  # 8. 上傳血壓測量結果 
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 創建血壓
            User_Pressure.objects.create(
                user=User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]),
                systolic=data["systolic"], diastolic=data["diastolic"], 
                pulse=data["pulse"], recorded_at=data["recorded_at"]
            )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def weight(request):  # 9. 上傳體重測量結果
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 創建體重
            User_Weight.objects.create(
                user=User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]),
                weight=data["weight"], body_fat=data["body_fat"], 
                bmi=data["bmi"], recorded_at=data["recorded_at"]
            )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def sugar(request):  # 10. 上傳血糖 
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 創建血糖
            User_Sugar.objects.create(
                user=User_account.objects.get(
                    id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]), 
                    sugar=data["sugar"], timeperiod=data["timeperiod"], 
                    recorded_at=data["recorded_at"]
            )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def diary_get(request):  # 14. 日記列表資料
    if request.method == "GET":
        try:
            user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            # 取得日記資料
            user_account = User_account.objects.get(id=user_id)
            user_sugar = User_Sugar.objects.filter(user=user_account)
            user_pressure = User_Pressure.objects.filter(user=user_account)
            user_weight = User_Weight.objects.filter(user=user_account)
            user_diet = User_diet.objects.filter(user=user_account)
            user_diary = list()
            for i in user_pressure:
                user_diary.append({
                    "id": i.id,
                    "user_id": user_id,
                    "systolic": i.systolic,
                    "diastolic": i.diastolic,
                    "pulse": i.pulse,
                    "recorded_at": i.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "blood_pressure"
                })
            
            for i in user_weight:
                user_diary.append({
                    "id": i.id,
                    "user_id": user_id,
                    "weight": float(i.weight),
                    "body_fat": float(i.body_fat),
                    "bmi": float(i.bmi),
                    "recorded_at": i.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "weight"
                })
            for i in user_sugar:
                user_diary.append({
                    "id": i.id,
                    "user_id": user_id,
                    "sugar": i.sugar,
                    "recorded_at": i.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "blood_sugar" 
                })
            for i in user_diet:
                user_diary.append({
                    "id": i.id,
                    "user_id": user_id,
                    "description": i.description,
                    "meal": i.meal, 
                    "tag": i.tag,
                    "lat": float(i.lat),
                    "lng": float(i.lng),
                    "image": i.image,
                    "recorded_at": i.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "diet"
                })
        except Exception as e:
            return JsonResponse({"status": "1"})
    return JsonResponse({"status": "0", "diary": user_diary})


@ csrf_exempt
def diet(request):  # 15. 飲食日記 
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 創建日記資料
            User_diet.objects.create(
                user=User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]), 
                description=data["description"], meal=data["meal"], 
                tag=" ".join(data["tag"]), image=data["image"], 
                lat=str(data["lat"]), lng=str(data["lng"]), 
                recorded_at=data["recorded_at"]
            )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def last_upload(request):  # 最後上傳時間 (11/17)
    if request.method == "GET":
        try:
            user_id = Session.objects.get(pk=request.headers["token"]).get_decoded()["id"]
            # 取得最後上傳時間
            user_last_uploat = {
                "blood_pressure": (User_Weight.objects.filter(user=User_account.objects.get(id=user_id)).latest('recorded_at').recorded_at).strftime("%Y-%m-%d %H:%M:%S"),
                "weight": (User_Pressure.objects.filter(user=User_account.objects.get(id=user_id)).latest('recorded_at').recorded_at).strftime("%Y-%m-%d %H:%M:%S"),
                "blood_sugar": (User_Sugar.objects.filter(user=User_account.objects.get(id=user_id)).latest('recorded_at').recorded_at).strftime("%Y-%m-%d %H:%M:%S"),
                "diet": (User_diet.objects.filter(user=User_account.objects.get(id=user_id)).latest('recorded_at').recorded_at).strftime("%Y-%m-%d %H:%M:%S")}
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0", "last_upload": user_last_uploat})


@ csrf_exempt
def records(request):  # 上一筆紀錄資訊(ok)
    try:
        user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
        # 取得上一筆資料
        user_account = User_account.objects.get(id=user_id)
        if request.method == "POST":
            if User_Sugar.objects.filter(user=user_account).exists():
                data = User_Sugar.objects.filter(user=user_account).latest('recorded_at')
                sugar_data = {
                    "id": data.id,
                    "user_id": user_id,
                    "sugar": data.sugar,
                    "recorded_at": data.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            if User_Pressure.objects.filter(user=user_account).exists():
                data = User_Pressure.objects.filter(user=user_account).latest('recorded_at')
                pressure_data = {
                    "id": data.id,
                    "user_id": user_id,
                    "systolic": data.systolic,
                    "diastolic": data.diastolic,
                    "pulse": data.pulse,
                    "recorded_at": data.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            if User_Weight.objects.filter(user=user_account).exists():
                data = User_Weight.objects.filter(user=user_account).latest('recorded_at')
                weight_data = {
                    "id": data.id,
                    "user_id": user_id,
                    "weight": float(data.weight),
                    "body_fat": float(data.body_fat),
                    "bmi": float(data.bmi),
                    "recorded_at": data.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            return JsonResponse({"status": "0", "blood_sugars": sugar_data, "blood_pressures": pressure_data, "weights":weight_data})
        if request.method == "DELETE":
            # 刪除對應路徑
            data = json.loads(request.body)
            if data.setdefault("blood_pressures", "Null") != "Null":
                for i in data["blood_pressures"]:
                    User_Pressure.objects.filter(user=user_account, id=i).delete()
            elif data.setdefault("blood_sugars", "Null") != "Null":
                for i in data["blood_sugars"]:
                    User_Sugar.objects.filter(user=user_account, id=i).delete()
            elif data.setdefault("weights", "Null") != "Null":
                for i in data["weights"]:
                    User_Weight.objects.filter(user=user_account, id=i).delete()
            elif data.setdefault("diets", "Null") != "Null":
                for i in data["diets"]:
                    User_diet.objects.filter(user=user_account, id=i).delete()
            return JsonResponse({"status": "0"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@ csrf_exempt
def a1c(request):  # 32. & 33. & 34. 糖化血色素
    try:
        user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
        user_account = User_account.objects.get(id=user_id)
        if request.method == "POST":
            data = json.loads(request.body)
            # 創建血色素
            User_a1c.objects.create(
                user=user_account,
                a1c=data["a1c"], 
                recorded_at=data["recorded_at"], 
                created_at=timezone.now().isoformat(timespec="seconds")
            )
            return JsonResponse({"status": "0"})        
        if request.method == "GET":
            # 取得血色素
            data_list = [
                {
                    {
                        "id": data.id, "user_id": user_id, "a1c": data.a1c, 
                        "recorded_at": data.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                } 
                for data in User_a1c.objects.filter(user=user_account)
            ]
            return JsonResponse({"status": "0", "a1cs": data_list})
        if request.method == "DELETE":
            data = json.loads(request.body)
            for i in data["ids"]:
                 User_a1c.objects.filter(user=user_account, id=i).delete()
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def drug_used(request):  # 41. 上傳藥物資訊 
    try:
        user_account = User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"])
        if request.method == "POST":
            data = json.loads(request.body)
            User_drug.objects.create(
                user=user_account, type=data["type"], 
                name=data["name"], recorded_at=data["recorded_at"]
            )
            return JsonResponse({"status": "0"})
        if request.method == "GET":
            data_list = []
            for data in User_drug.objects.filter(user=user_account):
                data_list.append(
                    {
                        "id": data.id,
                        "user_id": user_account.id,
                        "type": data.type,
                        "name": data.name,
                        "recorded_at": data.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
            return JsonResponse({"status": "0", "drug_useds": data_list})
        if request.method == "DELETE":
            data = json.loads(request.body)
            for t in data["ids"]:
                User_drug.objects.filter(user=user_account, id=t).delete()
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def medical(request):  # 更新就醫資訊(ok)
    try:
        user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
        user_account = User_account.objects.get(id=user_id)
        if request.method == "PATCH":
            data = json.loads(request.body)
            User_medical.objects.update(
                user=user_account, 
                diabetes_type=data["diabetes_type"], 
                oad=data["oad"], 
                insulin=data["insulin"], 
                anti_hypertensives=data["anti_hypertensives"]
            )   
            return JsonResponse({"status": "0"})
        if request.method == "GET":
            medical = User_medical.objects.get(user=user_account)
            medical_data = {
                "id": medical.id,
                "user_id": user_id,
                "diabetes_type": medical.diabetes_type,
                "oad": medical.oad,
                "insulin": medical.insulin,
                "anti_hypertensives": medical.anti_hypertensives,
                "created_at": medical.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            return JsonResponse({"status": "0", "medical_info": medical_data})
    except Exception as e:
        print(e)
        return JsonResponse({"status": "1"})


@ csrf_exempt
def friend_id_get(request):  # 16. 獲取控糖團邀請碼
    if request.method == "GET":
        try:
            user_friend_id = User_account.objects.get(
                id=Session.objects.get(
                    pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]).friend_id
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0", "invite_code": user_friend_id})


@ csrf_exempt
def friend_id_send(request):  # 19. 送出控糖團邀請 (
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_account = User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"])
            firend_user_account = User_account.objects.get(friend_id=data["invite_code"])
            now_time = timezone.now().isoformat(timespec="seconds")
            if User_friend.objects.filter(user=user_account, friend_id=data["invite_code"]).exists():
                return JsonResponse({"status": "2"})
            else:
                User_friend_request.objects.create(
                    user=firend_user_account, 
                    type=data["type"], 
                    friend_id=user_account.friend_id, 
                    created_at=now_time, 
                    updated_at=now_time
                )
                return JsonResponse({"status": "0"})
        except Exception as e:
            return JsonResponse({"status": "1"})


@ csrf_exempt
def friend_id_requests(request):  # 18. 獲取控糖團邀請
    if request.method == "GET":
        try:
            user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            user_account = User_account.objects.get(id=user_id)
            data_list = []
            for data in User_friend_request.objects.filter(user=user_account):
                request_user = User_account.objects.get(friend_id=data.friend_id)
                request_user_set = User_set.objects.get(user=request_user)
                if data.status == "0":
                    data_list.append(
                        {
                            "id": data.id,
                            "user_id": user_id,
                            "relation_id": user_account.friend_id,
                            "type": data.type,
                            "status": "0",
                            "created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at": data.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "user": {
                                "id": request_user.id,
                                "name": request_user_set.name,
                                "account": request_user.account,
                                "email": request_user_set.email,
                                "phone": request_user_set.phone,
                                "birthday": request_user_set.birthday.strftime("%Y-%m-%d %H:%M:%S"),
                                "height": request_user_set.height,
                                "gender": request_user_set.gender,
                                "created_at": request_user_set.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                "updated_at": request_user_set.updated_at.strftime("%Y-%m-%d %H:%M:%S")}
                        }
                    )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0", "requests": data_list})


@ csrf_exempt
def friend_accept(request, accept):  # 20.接受控糖團邀請
    if request.method == "GET":
        try:
            now_time = timezone.now().isoformat(timespec="seconds")
            user_account = User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"])
            friend_request = User_friend_request.objects.get(user=user_account, id=accept)
            friend_request.status = "1"
            friend_request.updated_at = now_time
            friend_request.save()
            User_friend.objects.create(
                user=user_account, 
                friend_id=friend_request.friend_id, 
                created_at=now_time, 
                updated_at=now_time, 
                status="1", 
                type=friend_request.type
            )
            User_friend.objects.create(
                user=User_account.objects.get(friend_id=friend_request.friend_id), 
                friend_id=user_account.friend_id, 
                created_at=now_time, 
                updated_at=now_time, 
                status="1", 
                type=friend_request.type
            )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def friend_refuse(request, refuse):  # 拒絕控糖團邀請(OK)
    if request.method == "GET":
        try:
            user_account = User_account.objects.get(
                id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"])
            User_friend_request.objects.filter(user=user_account, id=refuse).update(status="2")
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def friend_remove(request, uid):  # 用不到
    if request.method == "DELETE":
        try:
            user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            User_friend_request.objects.filter(
                user=User_account.objects.get(id=user_id), 
                friend_id=User_account.objects.get(id=uid).friend_id).delete()
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def friend_list(request):  # 17. 控糖團列表
    if request.method == "GET":
        try:
            user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            data_list = []
            for data in User_friend.objects.filter(user=User_account.objects.get(id=user_id)):
                request_user = User_account.objects.get(friend_id=data.friend_id)
                request_user_set = User_set.objects.get(user=request_user)
                data_list.append(
                    {
                        "id": data.id,
                        "name": request_user_set.name,
                        "account": request_user.account,
                        "email": request_user.email,
                        "status": data.status,
                        "birthday": request_user_set.birthday.strftime("%Y-%m-%d %H:%M:%S"),
                        "height": request_user_set.height,
                        "gender": request_user_set.gender,
                        "created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": data.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "relation_type": data.type
                    }
                )
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0", "friends": data_list})


@ csrf_exempt
def friend_delete(request):  # 刪除更多好友
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user_account = User_account.objects.get(id=Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"])
            user_friend_data = User_friend.objects.get(user=user_account, id=data["ids[]"])
            User_friend.objects.get(user=User_account.objects.get(friend_id=user_friend_data.friend_id), friend_id=user_account.friend_id).delete()
            User_friend.objects.get(user=user_account, friend_id=user_friend_data.friend_id).delete()
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def friend_request_result(request):  # 控糖團結果
    if request.method == "GET":
        try:
            user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            data_list = []
            for data in User_friend_request.objects.filter(user=User_account.objects.get(id=user_id)):
                request_user = User_account.objects.get(friend_id=data.friend_id)
                request_user_set = User_set.objects.get(user=request_user)
                data_list.append(
                    {
                        "id": data.id,
                        "user_id": user_id,
                        "relation_id": request_user.id,
                        "type": data.type,
                        "status": data.status,
                        "read": "true",
                        "created_at":  data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": data.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "relation": {
                            "id": request_user.id,
                            "name": request_user_set.name,
                            "account": request_user.account,
                            "email": request_user.email,
                            "fb_id": request_user_set.fcm_id,
                            "status": data.status,
                            "birthday": request_user_set.birthday.strftime("%Y-%m-%d %H:%M:%S"),
                            "height": request_user_set.height,
                            "gender": request_user_set.gender,
                            "created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at": data.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                )
        except Exception as e:
            return JsonResponse({"status": "1",  "results": data_list})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def care(request):  # 發送關懷諮詢
        try:
            user_id = Session.objects.get(pk=request.headers["Authorization"].split(" ")[1]).get_decoded()["id"]
            user_account = User_account.objects.get(id=user_id)
            now_time = timezone.now().isoformat(timespec="seconds")
            if request.method == "POST":
                data = json.loads(request.body)
                Care_message.objects.create(user=user_account, message=data["message"], reply_id=user_id, created_at=now_time, updated_at=now_time)
                return JsonResponse({"status": "0"})
            if request.method == "GET":
                data_list = []
                for data in Care_message.objects.filter(user=user_account):
                    data_list.append(
                        {
                            "id": data.id,
                            "user_id": user_id,
                            "member_id": "1",
                            "reply_id": data.reply_id,
                            "message": data.message,
                            "created_at": data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "updated_at": data.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                        }
                    )
                return JsonResponse({"status": "0",  "cares": data_list})
        except Exception as e:
            return JsonResponse({"status": "1"})


@ csrf_exempt
def notification(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = Session.objects.get(
                pk=request.headers["token"]).get_decoded()["id"]
            Care_message.objects.create(
                user=User_account.objects.get(id=user_id), 
                message=data["message"], reply_id=user_id, 
                created_at=time.strftime("%Y-%m-%d %H:%M:%S", 
                time.localtime()), 
                updated_at=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        except Exception as e:
            return JsonResponse({"status": "1"})
        return JsonResponse({"status": "0"})


@ csrf_exempt
def badge(request):
    try:
        if request.method == "PUT":
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def share(request):
    try:
        if request.method == "POST":
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def share_0(request):
    try:
        if request.method == "GET":
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def share_1(request):
    try:
        if request.method == "GET":
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def share_2(request):
    try:
        if request.method == "GET":
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})


@ csrf_exempt
def news(request):
    try:
        if request.method == "GET":
            return JsonResponse({"status": "0"})
    except Exception as e:
        return JsonResponse({"status": "1"})