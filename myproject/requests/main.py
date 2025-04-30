# FastAPI 라이브러리에서 FastAPI 클래스를 가져온다
from fastapi import FastAPI

# Optional 타입을 사용하기 위해 typing 모듈에서 Optional을 가져온다
# (어떤 값이 있을 수도 있고, 없을 수도 있다를 표현할 때 사용)
from typing import Optional

# FastAPI 앱 인스턴스를 만든다 (이 앱이 서버 역할을 한다)
app = FastAPI()

# 가짜 데이터베이스처럼 사용할 리스트를 만든다
# 각 아이템은 'item_name'이라는 키를 가진 딕셔너리 형태
fake_items_db = [
    {"item_name": "Foo"},  # 첫 번째 아이템
    {"item_name": "Bar"},  # 두 번째 아이템
    {"item_name": "Baz"}   # 세 번째 아이템
]

# --------------------------------------------

# GET 요청으로 '/items' 경로에 접속하면 실행되는 함수
@app.get("/items")
async def read_items(skip: int = 0, limit: int = 2):
    """
    - skip: 몇 개를 건너뛸지 (디폴트 0)
    - limit: 최대 몇 개를 가져올지 (디폴트 2)
    """
    # 리스트의 특정 부분만 잘라서 반환한다
    # 예: skip=0, limit=2 → fake_items_db[0:2] → Foo, Bar
    return fake_items_db[skip : skip + limit]

# --------------------------------------------

# GET 요청으로 '/items_nd/' 경로에 접속하면 실행되는 함수
@app.get("/items_nd/")
async def read_item_nd(skip: int, limit: int):
    """
    - skip: 몇 개 건너뛸지 (반드시 쿼리 파라미터로 줘야 함)
    - limit: 몇 개 가져올지 (반드시 쿼리 파라미터로 줘야 함)
    
    ※ 여기서는 기본값이 없기 때문에
    → 무조건 URL에 ?skip=1&limit=2 처럼 값을 줘야 한다!
    """
    return fake_items_db[skip : skip + limit]

# --------------------------------------------

# GET 요청으로 '/items/{item_id}' 경로에 접속하면 실행되는 함수
# 중괄호 {} 안에 들어가는 것은 '경로 파라미터'라고 부른다
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    """
    - item_id: 주소 경로에서 숫자(id)를 가져온다
    - q: (선택사항) 추가로 물어볼 내용 (query 파라미터)

    예: /items/3?q=hello
    - item_id: 3
    - q: "hello"
    """
    item = {"item_id": item_id}  # 아이템 기본 데이터 만들기
    if q:  # 만약 q 값이 있다면
        item.update({"q": q})  # 딕셔너리에 q 값 추가
    return item  # 완성된 딕셔너리 반환

# --------------------------------------------

# GET 요청으로 '/items/name' 경로에 접속하면 실행되는 함수
@app.get("/items/name")
async def read_item_name(skip: int = 0, limit: int | None = None):
    """
    - skip: 기본은 0 (몇 개를 건너뛸지)
    - limit: 기본은 None (제한 없이 전부 가져온다는 뜻)

    limit이 있으면 → skip부터 limit까지 가져온다
    limit이 없으면 → 'limit is None' 메시지를 반환한다
    """
    if limit:
        return fake_items_db[skip : skip + limit]  # 부분 리스트 반환
    else:
        return {"limit is None"}  # limit 없을 때 메시지 반환

# --------------------------------------------
