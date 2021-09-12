# api/datdabase.py
from mongoengine import connect
from api.models import RankModel
 

MONGO_DTATBASE="graphql-example"
MONGO_HOST="mongodb://localhost:27017"
# mongomock://localhost
# mongodb://localhost:27017
# Database 연결
conn = connect(MONGO_DTATBASE, host=MONGO_HOST, alias="default")
print(conn)
# 기초 데이터 Insert 함수
def init_db():
	print('mongo setting')

	rank = RankModel(name="kim", mode="3x3", score=2, is_mobile=False, reg_dttm="20200413170848")
	rank.save() # Insert
 
	rank = RankModel(name="choi", mode="3x3", score=128, is_mobile=False, reg_dttm="20200413170848")
	rank.save() # Insert

	rank = RankModel(name="lee", mode="4x4", score=1024, is_mobile=False, reg_dttm="20200413170848")
	rank.save() # Insert

	rank = RankModel(name="heo", mode="4x4", score=16, is_mobile=False, reg_dttm="20200413170848")
	rank.save() # Insert