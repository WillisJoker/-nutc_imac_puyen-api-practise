from email import message
from django.db import models
from django.contrib.auth.models import AbstractUser
import ast
import django.utils.timezone as timezone
# Create your models here.


class User_account(AbstractUser):
    id = models.CharField(max_length=150, primary_key=True)
    account = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    password = models.CharField(max_length=150, null=False)
    mail_id = models.CharField(max_length=32)
    account_ck = models.BooleanField(default=False)
    friend_id = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    must_change_password = models.BooleanField(default=False)


class User_set(models.Model):
    user = models.ForeignKey(User_account, on_delete=models.CASCADE, related_name='set')
    name = models.CharField(max_length=150, default="未填寫")
    birthday =  models.DateField(default=timezone.now)
    height = models.IntegerField(default="0")
    gender = models.CharField(max_length=150, default="未填寫")
    fcm_id = models.CharField(max_length=150, default="未填寫")
    address = models.CharField(max_length=150, default="未填寫")
    weight = models.CharField(max_length=150, default="0")
    phone = models.CharField(max_length=150, default="未填寫")
    email = models.CharField(max_length=150, default="未填寫")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class User_default(models.Model):
    user = models.ForeignKey(User_account, on_delete=models.CASCADE, related_name='preset')
    sugar_delta_max = models.IntegerField(default=0)
    sugar_delta_min = models.IntegerField(default=-1)
    sugar_morning_max = models.IntegerField(default=0)
    sugar_morning_min = models.IntegerField(default=-1)
    sugar_evening_max = models.IntegerField(default=0)
    sugar_evening_min = models.IntegerField(default=-1)
    sugar_before_max = models.IntegerField(default=0)
    sugar_before_min = models.IntegerField(default=-1)
    sugar_after_max = models.IntegerField(default=0)
    sugar_after_min = models.IntegerField(default=-1)
    systolic_max = models.IntegerField(default=0)
    systolic_min = models.IntegerField(default=-1)
    diastolic_max = models.IntegerField(default=0)
    diastolic_min = models.IntegerField(default=-1)
    pulse_max = models.IntegerField(default=0)
    pulse_min = models.IntegerField(default=-1)
    weight_max = models.IntegerField(default=0)
    weight_min = models.IntegerField(default=-1)
    bmi_max = models.IntegerField(default=0)
    bmi_min = models.IntegerField(default=-1)
    body_fat_max = models.IntegerField(default=0)
    body_fat_min = models.IntegerField(default=-1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class User_put(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='put')
    after_recording = models.BooleanField(default=False)
    no_recording_for_a_day = models.BooleanField(default=False)
    over_max_or_under_min = models.BooleanField(default=False)
    after_meal = models.BooleanField(default=False)
    unit_of_sugar = models.BooleanField(default=False)
    unit_of_weight = models.BooleanField(default=False)
    unit_of_height = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class User_Pressure(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='pressure')
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    pulse = models.IntegerField()
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class User_Weight(models.Model):
    user = models.ForeignKey(User_account, on_delete=models.CASCADE, related_name='weight')
    weight = models.CharField(max_length=150)
    body_fat = models.CharField(max_length=150)
    bmi = models.CharField(max_length=150)
    recorded_at = models.DateTimeField()


class User_Sugar(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='sugar')
    sugar = models.IntegerField()
    timeperiod = models.IntegerField()
    recorded_at = models.DateTimeField()


class User_diet(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='diet')
    description = models.CharField(max_length=150)
    meal = models.IntegerField()
    tag = models.CharField(max_length=150)
    lat = models.CharField(max_length=150)
    lng = models.CharField(max_length=150)
    image = models.IntegerField()
    recorded_at = models.DateTimeField()


class Test_db(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='test')
    m_url = models.ImageField(upload_to='image/')


class User_a1c(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='a1c')
    a1c = models.CharField(max_length=150)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class User_drug(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='drug')
    type = models.BooleanField()
    name = models.CharField(max_length=150)
    recorded_at = models.DateTimeField()


class User_medical(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='medical')
    diabetes_type = models.IntegerField(default=0)
    oad = models.BooleanField(default=False)
    insulin = models.BooleanField(default=False)
    anti_hypertensives = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class User_friend(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='friend')
    friend_id = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    type = models.IntegerField(default="0")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class User_friend_request(models.Model):
    user = models.ForeignKey(User_account, on_delete=models.CASCADE, related_name='request')
    type = models.IntegerField(default="0")
    friend_id = models.CharField(max_length=150)
    status = models.CharField(max_length=150, default="0")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Care_message(models.Model):
    user = models.ForeignKey(
        User_account, on_delete=models.CASCADE, related_name='message')
    message = models.CharField(max_length=150)
    reply_id = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
