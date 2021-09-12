# app.py
import dotenv
from api import create_app
from api.database import init_db
 
 
if __name__ == '__main__':
  # 환경변수 설정
  dotenv.load_dotenv(dotenv_path=".env")
  
  # MongoDB 접속 및 기초 데이터 입력
  init_db()
  
  # Flask App 실행
  app = create_app()
  app.run(host="localhost", port=3000)