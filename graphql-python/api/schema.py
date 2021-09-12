
# api/schema.py
import graphene
 
from api.models import RankModel, RankType
 
# Query 설정
class Query(graphene.ObjectType):  
  # 모든 랭킹 목록.
  ranks = graphene.List(RankType)
  
  # 특정 모드에 대한 랭킹 목록.
  ranks_for_mode = graphene.List(RankType, mode=graphene.String(required=True))
  
  # 특정 랭킹에 대한 정보.
  rank = graphene.Field(RankType, id=graphene.String(required=True))
 
  # MongoDB에서 모든 랭킹 목록을 조회
  def resolve_ranks(parent, info):
    return RankModel.objects.all()
    
  # MongoDB에서 특정 모드의 모든 랭킹 목록을 조회
  def resolve_ranks_for_mode(parent, info, mode):
    return RankModel.objects(mode=mode).all()
 
  # MongoDB에서 특정 랭킹을 조회.
  def resolve_rank(parent, info, id):
    return RankModel.objects.get(id=id)
 
# Schema 생성
schema = graphene.Schema(
  query=Query,
  types=[
    RankType
  ]
)
