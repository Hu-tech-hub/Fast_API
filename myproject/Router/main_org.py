# FastAPI 프레임워크에서 서버를 실행하고 라우팅을 관리하기 위한 핵심 클래스
from fastapi import FastAPI

# 데이터 모델 정의 및 유효성 검사, 자동 문서화를 지원하는 Pydantic의 기반 클래스
from pydantic import BaseModel

# FastAPI 인스턴스 생성 → 이 객체가 전체 API 앱의 엔트리포인트 역할을 함
app = FastAPI()

# ----- 📦 데이터 모델 정의 -----
class Item(BaseModel):
    name: str                         # 필수 필드: 상품 이름 (문자열)
    description: str = None          # 선택 필드: 설명 (기본값은 None)
    price: float                     # 필수 필드: 가격 (실수형)
    tax: float = None                # 선택 필드: 세금 (실수형, 없어도 됨)

    '''
    💡 BaseModel을 상속한 클래스는 다음과 같은 기능을 가짐:
    - JSON 요청을 자동으로 Python 객체로 변환
    - 데이터 타입 및 필수 여부 자동 검사
    - Swagger UI(/docs)에 자동 문서화됨
    '''

# ----- ✅ GET: 단일 아이템 조회 -----
@app.get("/item/{item_id}")  # 경로 매개변수(Path Parameter): /item/10 같은 URL 요청 처리
async def read_item(item_id: int):   # item_id는 URL에서 받아온 정수형 값
    return {"item_id": item_id}      # 단순히 받은 ID를 JSON으로 반환 (DB 연동 없음)

# ----- ✅ POST: 아이템 생성 -----
@app.post("/item")
async def create_item(item: Item):  # 요청 본문에 포함된 JSON 데이터를 Item 모델로 파싱
    return item                      # 받은 데이터를 그대로 응답으로 반환 (Echo API)

# ----- ✅ PUT: 아이템 수정 -----
@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item):
    '''
    - item_id: URL 경로에서 받은 아이템 ID
    - item: 요청 본문에서 받은 아이템 정보
    - 둘을 묶어 응답 JSON에 담아 반환함
    '''
    return {"item_id": item_id, "item": item}

# ----- ✅ GET: 전체 사용자 목록 조회 -----
@app.get("/users/")
async def read_users():
    # 고정된 사용자 목록을 리스트로 반환
    return [{"username": "Rickie"}, {"username": "Martin"}]

# ----- ✅ GET: 현재 로그인된 사용자 정보 조회 -----
@app.get("/users/me")
async def read_user_me():
    # 인증 기능이 없으므로 항상 동일한 사용자 정보 반환
    return {"username": "currentuser"}

# ----- ✅ GET: 특정 사용자 조회 -----
@app.get("/users/{username}")
async def read_user(username: str):  # 경로 매개변수로 사용자 이름을 문자열로 받음
    return {"username": username}    # 입력된 사용자 이름을 그대로 반환
