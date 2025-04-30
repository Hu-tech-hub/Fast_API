# FastAPI 핵심 모듈
from fastapi import FastAPI, Request

# HTML을 응답으로 보내기 위한 모듈
from fastapi.responses import HTMLResponse

# 정적 파일(css, js, 이미지 등)을 서빙하기 위한 모듈
from fastapi.staticfiles import StaticFiles

# 템플릿 렌더링을 위한 Jinja2 연동 모듈
from fastapi.templating import Jinja2Templates

# FastAPI 인스턴스 생성 (웹 애플리케이션 객체)
app = FastAPI()

# ----------------------------- 정적 파일 설정 -----------------------------
# URL 경로 "/static"으로 들어온 요청에 대해
# 실제 파일 시스템의 "static/" 폴더에서 파일을 찾아 응답하도록 설정
# 예: 브라우저가 "/static/logo.png" 요청 시 → static/logo.png 파일 전송
# name="static" 은 템플릿 안에서 url_for("static", path="...") 으로 참조할 수 있게 이름 지정
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------- 템플릿 설정 -----------------------------
# Jinja2 템플릿 엔진을 사용하도록 설정
# "templates" 폴더 안의 HTML 파일을 동적으로 렌더링 가능하게 함
templates = Jinja2Templates(directory="templates")


# ----------------------------- 라우터 함수 정의 -----------------------------
# /items/{id} 로 요청이 들어오면 실행되는 비동기 함수
# 예: /items/7?q=test → id는 7, q는 "test" 로 받아짐
# HTML을 반환해야 하므로 response_class=HTMLResponse 지정
@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None):
    """
    📌 URL 구조
        /items/{id} → Path Parameter
        ?q=abc → Query Parameter

    🔧 파라미터 설명
        - request: FastAPI가 템플릿 렌더링에 꼭 필요로 하는 Request 객체
        - id: URL 경로에서 받아온 값 (Path Parameter)
        - q: ?q=... 형식으로 URL 뒤에 붙는 선택적 Query Parameter

    🧠 처리 방식
        1. 어떤 템플릿을 사용할지 html_name으로 지정
        2. templates.TemplateResponse()를 호출하여 HTML 렌더링
        3. context는 템플릿 내부에서 사용할 변수들을 담은 딕셔너리

    📄 템플릿 내부 예시 사용법:
        {{ id }}, {{ q_str }} 로 context의 값을 출력
        <img src="{{ url_for('static', path='logo.png') }}"> 로 정적 이미지 출력 가능
    """

    html_name = "read_static.html"  # 사용할 템플릿 파일 이름 (templates/ 디렉토리 내에 존재해야 함)
    # html_name = "item_urlfor.html"  # 대체 템플릿 (주석처리된 부분)

    return templates.TemplateResponse(
        request=request,             # 반드시 request 객체 포함 (Jinja2 요구사항)
        name=html_name,             # 사용할 템플릿 파일 이름
        context={
            "id": id,               # 템플릿에서 사용할 id 값
            "q_str": q              # 템플릿에서 사용할 쿼리 파라미터
        }
    )
