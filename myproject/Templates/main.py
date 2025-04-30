# FastAPI에서 필요한 것들을 불러온다
from fastapi import FastAPI, Request  # 웹 요청(Request) 처리용
from fastapi.responses import HTMLResponse  # HTML을 화면에 보여주기 위해
from fastapi.templating import Jinja2Templates  # HTML 템플릿 사용을 위한 도구
from pydantic import BaseModel  # 데이터를 깔끔하게 표현해주는 도구

# FastAPI 앱 만들기! (이게 서버 본체야)
app = FastAPI()

# "templates" 폴더 안에 있는 HTML 파일들을 사용할 수 있도록 준비해준다
templates = Jinja2Templates(directory="Templates")

# 물건(Item)을 표현하기 위한 틀을 만든다 (이걸 '모델'이라고 해)
# 물건에는 이름(name)과 가격(price)이 있다는 뜻이야
class Item(BaseModel):
    name: str      # 물건 이름: 글자
    price: float   # 물건 가격: 숫자

# 이건 URL에 "/items/어떤아이디"라고 접속하면 실행되는 함수야
# 예: /items/5?q=abc
# response_class=HTMLResponse는 "이건 HTML로 보여줄 거야!"라고 알려주는 것
@app.get("/items/{id}", response_class=HTMLResponse)
# 이 함수가 실행되려면 꼭 Request(요청)라는 정보를 받아야 해!
# 그리고 id는 주소에 있는 값, q는 물음표 뒤에 붙는 선택적인 값이야
async def read_item(request: Request, id: str, q: str | None = None):
    # 물건을 하나 만든다 (이름은 test_item, 가격은 10)
    item = Item(name="test_item", price=10)
    
    # 물건을 딕셔너리 형태로 바꾼다 (HTML에서 쉽게 쓰려고)
    item_dict = item.model_dump()

    # HTML 파일(item.html)을 보여주면서 데이터를 넘겨준다
    return templates.TemplateResponse(
        request=request,            # 요청 정보
        name="item.html",           # 보여줄 HTML 파일 이름
        context={                   # HTML에서 사용할 변수들을 담은 곳
            "id": id,               # 주소에 있던 id 값
            "q_str": q,             # 물음표 뒤에 있던 q 값 (없을 수도 있음)
            "item": item,           # 만든 물건 객체
            "item_dict": item_dict  # 딕셔너리로 바꾼 물건 정보
        }
    )

# 위 코드처럼 쓸 수 있지만, FastAPI 옛날 버전에서는 아래처럼 써야 했어
# return templates.TemplateResponse(name="item.html",
#                                   {"request": request, "id": id, ... })

# 이건 "/item_gubun" 주소로 접속할 때 실행돼
# 예: /item_gubun?gubun=fruit
@app.get("/item_gubun")
async def read_item_by_gubun(request: Request, gubun: str):
    # 물건 하나 만들기 (이름은 test_item_02, 가격은 4.0)
    item = Item(name="test_item_02", price=4.0)
    
    # HTML 파일(item_gubun.html)을 보여주며 데이터 전달
    return templates.TemplateResponse(
        request=request, 
        name="item_gubun.html", 
        context={           # HTML에서 쓸 변수들
            "gubun": gubun, # 주소에서 받은 gubun 값
            "item": item    # 만든 물건 객체
        }
    )

# 이건 "/all_items" 주소로 접속하면 실행돼 (모든 물건들을 보여줄 거야!)
@app.get("/all_items", response_class=HTMLResponse)
async def read_all_items(request: Request):
    # 여러 개의 물건을 리스트로 만들기 (test_item_0 ~ test_item_4까지)
    all_items = [Item(name="test_item_" + str(i), price=i) for i in range(5)]
    
    # 만든 물건들을 콘솔에 출력해본다 (개발자가 확인용으로 보는 것)
    print("all_items:", all_items)
    
    # HTML 파일(item_all.html)을 보여주며 물건 리스트 전달
    return templates.TemplateResponse(
        request=request, 
        name="item_all.html", 
        context={"all_items": all_items}  # HTML에서 사용할 물건 목록
    )

# 이건 "/read_safe" 주소로 접속하면 실행돼 (안전하게 HTML을 보여주는 예시야)
@app.get("/read_safe", response_class=HTMLResponse)
async def read_safe(request: Request):
    # 보여줄 HTML 내용 (ul과 li는 HTML 태그야, 리스트처럼 보여줘)
    html_str = '''
    <ul>
    <li>튼튼</li>
    <li>저렴</li>
    </ul>
    '''
    
    # read_safe.html 템플릿 파일에서 html_str이라는 변수로 이 내용을 사용하게 해줘
    return templates.TemplateResponse(
        request=request, 
        name="read_safe.html", 
        context={"html_str": html_str}  # HTML에서 쓸 변수
    )
