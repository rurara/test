# api/__init__.py
from flask import Flask
from flask_graphql import GraphQLView
from api.schema import schema
 
def create_app():
  # Flask Application 생성
  app = Flask(__name__)
  
  # /graphql EndPoint 설정
  app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
      'graphql',
      schema=schema,
      graphiql=True   # gql 테스트 페이지 제공
    )
  )
  
  return app