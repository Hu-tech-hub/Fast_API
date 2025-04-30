from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Annotated

app = FastAPI()

# Pydantic은 FastAPI가 데이터를 깔끔하게 관리할 수 있게 도와주는 라이브러리야
# Item이라는 이름의 데이터 형식을 정의하고 있다
# Pydantic 모델을 만들 때는 반드시 BaseModel을 상속해야 한다!

class Item(BaseModel):
    name: str                        # name은 반드시 문자열(str)이어야 한다
    description: str | None = None    # description은 문자열 또는 None(없음)일 수 있다
    price: float                     # price는 반드시 소수점이 있는 숫자(float)여야 한다
    tax: float | None = None          # tax는 소수점 숫자거나 없을 수도 있다 (선택 사항)

class User(BaseModel):
    username: str                       # username은 반드시 문자열(str) 타입이어야 한다
    full_name: str | None = None         # full_name은 문자열이거나 없어도 된다
    #full_name: Optional[str] = None

# ---------------------------------------------------


#수행 함수의 인자로 Pydantic model이 입력되면 Json 형태의 Request Body 처리
@app.post("/items")
async def create_item(item: Item):
    print("###### item type:", type(item))
    print("###### item:", item)
    return item


@app.post("/items_tax/")
async def create_item_tax(item: Item):
    # 사용자가 보내준 JSON 데이터를 item이라는 Pydantic 모델로 자동 변환해서 받는다
    
    item_dict = item.model_dump()
    # model_dump() 메서드를 호출하면
    # item 안에 들어있는 데이터를 딕셔너리(dict) 형태로 변환해준다
    # 예시: {"name": "apple", "description": "red", "price": 3.0, "tax": 0.3}
    print("#### item_dict:", item_dict)
    # 변환된 딕셔너리를 출력해서 확인 (서버 콘솔에 찍힘)

    if item.tax:
        # 만약 tax 값이 있다면 (None이 아니라면)
        price_with_tax = item.price + item.tax
        # price와 tax를 더해서 최종 가격(price_with_tax)을 계산한다
        item_dict.update({"price_with_tax": price_with_tax})
        # 계산한 값을 item_dict에 새로운 키 "price_with_tax"로 추가한다

    return item_dict
    # 최종적으로 수정된 딕셔너리를 사용자에게 JSON 형태로 돌려준다

# ------------------------------------------
# Path, Query, Request Body를 모두 동시에 사용하는 예시

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    """
    - item_id: URL 경로(Path)에서 받는 값
    - item: JSON 데이터(Request Body)에서 받는 값
    - q: URL 쿼리 파라미터(Query Parameter)에서 받는 값
    """

    result = {"item_id": item_id, **item.model_dump()}
    # item_id를 딕셔너리에 추가하고
    # item 데이터(Item 모델)를 딕셔너리 형태로 풀어서 같이 추가한다
    # ( **item.model_dump() 는 name, description, price, tax 전부 펼쳐서 넣는다는 뜻)

    if q:
        result.update({"q": q})
        # 만약 쿼리 파라미터 q가 있으면, 그 값도 딕셔너리에 추가한다

    print("#### result:", result)
    # 서버 콘솔에 결과를 출력해본다 (개발자가 확인할 수 있게)

    return result
    # 최종 딕셔너리를 응답으로 돌려준다

# ------------------------------------------
# 여러 개의 Request Body를 동시에 받는 예시
# (item과 user 둘 다 JSON으로 받아야 함)

@app.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, user: User):
    """
    - item_id: URL 경로(Path)에서 받는 값
    - item: 첫 번째 JSON 데이터(Request Body)
    - user: 두 번째 JSON 데이터(Request Body)
    """

    results = {"item_id": item_id, "item": item, "user": user}
    # item_id와 함께, item과 user 객체 자체를 결과에 담는다
    # (FastAPI가 자동으로 item과 user를 JSON 형태로 변환해줄 거다)

    print("results:", results)
    # 서버 콘솔에 출력해서 확인

    return results
    # 최종 딕셔너리를 응답으로 돌려준다


