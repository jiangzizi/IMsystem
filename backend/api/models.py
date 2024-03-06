from django.db import models
from utils import utils_time
from django.contrib.auth.hashers import make_password,check_password
from utils.utils_require import MAX_CHAR_LENGTH, TELEPHONE_LENGTH
# Create your models here.

class User(models.Model):
    #TODO image storage
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH, unique=True)
    password = models.CharField(max_length=MAX_CHAR_LENGTH)
    register_time = models.FloatField(default=utils_time.get_timestamp)
    login_time=models.FloatField(default=utils_time.get_timestamp)
    email = models.EmailField(unique=True)  # 新增 email 字段
    telephone = models.CharField(max_length=TELEPHONE_LENGTH, unique=True)  # 新增 telephone 字段
    
    class Meta:
        indexes = [models.Index(fields=["name"])]
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self) -> str:
        return self.name