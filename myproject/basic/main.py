# FastAPI 라이브러리에서 FastAPI라는 클래스를 가져온다
from fastapi import FastAPI

# FastAPI라는 클래스를 이용해서 웹 어플리케이션을 만든다
# 여기서 app은 우리가 만든 FastAPI 프로그램이라고 생각하면 된다
app = FastAPI()

# ---------------------------------------------------

# @app.get("/")  
# → "GET" 방식으로 웹 주소의 "/" (루트, 홈페이지 같은 것) 에 요청이 오면
# → 이 밑에 있는 함수를 실행시킨다!
@app.get("/", tags=['Simple'], 
            summary="홈페이지", 
            description="홈페이지에 접속했을 때 보여주는 메시지")
def read_root():
    # 이 함수가 하는 일은
    # 그냥 "Hello, FastAPI!"라는 메시지를 딕셔너리 형태로 보내주는 것
    # 딕셔너리는 쉽게 말하면 {키:값} 쌍으로 된 데이터다
    return {"message": "Hello, FastAPI!"}

# ---------------------------------------------------

# ---------------------------------------------------
@app.get("/items/all")
def read_all_items():
    return {"message": "모든 아이템을 가져옵니다."}

# ---------------------------------------------------
# @app.get("/items/{item_id}")  
# → "GET" 방식으로 "/items/어떤숫자" 이런 식으로 요청이 오면
# → 이 밑에 있는 함수를 실행시킨다!
# 예시: "/items/3" 이런 주소로 접근하면 item_id가 3이 된다
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    # item_id는 주소에 있는 숫자를 가져온다
    # 예를 들면 "/items/5" 라고 하면 item_id는 5가 된다
    # (item_id: int → item_id는 '정수(int)' 타입이어야 한다는 뜻)

    # q는 추가로 받을 수 있는 '쿼리 파라미터'다
    # 예를 들어 "/items/5?q=hello" 이렇게 쓰면 q는 "hello"가 된다
    # (q: str = None → q는 '문자열(str)' 타입인데 없어도 된다 → 기본값은 None)

    # 결과로 item_id와 q 값을 딕셔너리 형태로 보내준다
    return {"item_id": item_id, "q": q}


