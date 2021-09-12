# api/models.py
import datetime
 
from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField
 
from graphene_mongo import MongoengineObjectType
 
# MongoDB Model
class RankModel(Document):
  meta = {'collection': 'ranking'}
  mode = StringField()
  name = StringField()
  score = IntField()
  is_mobile = BooleanField()
  reg_dttm = StringField()
  upd_dttm = StringField()
  
 
# Schema Type
class RankType(MongoengineObjectType):
  class Meta:
    model = RankModel
  
  # reg_dttm을 출력할 때 실행되는 로직. ( 날짜형식 변경 )
  def resolve_reg_dttm(parent, info, **kwargs):
    return datetime.datetime.strptime(parent.reg_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
 
  # upd_dttm을 출력할 때 실행되는 로직. ( 날짜형식 변경 )
  def resolve_upd_dttm(parent, info, **kwargs):
    return datetime.datetime.strptime(parent.upd_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    
