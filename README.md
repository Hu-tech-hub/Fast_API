
# 🚀 FastAPI 학습 저장소

이 저장소는 Python 기반 웹 프레임워크인 **FastAPI**를 학습하고 실습한 내용을 정리한 공간입니다.  
경로 파라미터, 쿼리 파라미터, 템플릿 엔진(Jinja2), 정적/동적 처리 방식 등 **실무에 자주 사용되는 기능 위주로 구성**되어 있습니다.

---

## 📌 주요 학습 내용

| 기능 | 설명 |
|------|------|
| ✅ FastAPI 기본 구조 | `FastAPI()`, `@app.get()`, Uvicorn 실행법 |
| ✅ Path Parameter | `/items/{id}` 형태로 URL 경로 값 받기 |
| ✅ Query Parameter | `?q=abc` 형태로 URL 쿼리 받기 |
| ✅ Jinja2 템플릿 연동 | HTML 페이지에 동적으로 값 삽입 |
| ✅ Pydantic 모델 | JSON 데이터를 구조화 및 검증 |
| ✅ 정적 vs 동적 처리 이해 | HTML 직접 반환 vs 템플릿 렌더링 |
| ✅ TemplateResponse | `request` 포함한 HTML 응답 생성 |

---

## 🛠️ 실행 방법

```bash
# 1. 가상환경 생성 및 진입
python -m venv venv
source venv/bin/activate   # 윈도우: venv\Scripts\activate

# 2. 필수 패키지 설치
pip install -r requirements.txt

# 3. 서버 실행
uvicorn main:app --reload --port=8000
```

브라우저에서 접속: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌐 API 문서 자동 생성

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 참고

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Jinja2 문법 정리](https://jinja.palletsprojects.com/)

---