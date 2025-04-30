from pydantic import BaseModel
from typing import Optional, Annotated
from fastapi import FastAPI, Form, Depends

app = FastAPI()

# 개별 Form data 값을 Form()에서 처리하여 수행함수 적용. 
# Form()은 form data값이 반드시 입력되어야 함. Form(None)과 Annotated[str, Form()] = None은 Optional
@app.post("/login")
async def login(username: str = Form(),
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"username": username, 
            "email": email,
            "country": country}

# ellipsis(...) 을 사용하면 form data값이 반드시 입력되어야 함. 
@app.post("/login_f/")
async def login(username: str = Form(...), 
                email: str = Form(...),
                country: Annotated[str, Form()] = None):
    return {"username": username, 
            "email": email, 
            "country": country}

# path, query parameter와 함께
@app.post("/login_pq/{login_gubun}")
async def login(login_gubun: int, q: str | None = None, 
                username: str = Form(), 
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"login_gubun": login_gubun,
            "q": q,
            "username": username, 
            "email": email, 
            "country": country}

#Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성. 
class Item(BaseModel):
    name: str
    description: str | None = None
    #description: Optional[str] = None
    price: float
    tax: float | None = None
    #tax: Optional[float] = None

# json request body용 end point
@app.post("/items_json/")
async def create_item_json(item: Item):
    return item

# form tag용 end point
@app.post("/items_form/")
async def create_item_json(name: str = Form(),
                        description: Annotated[str, Form()] = None,
                        price: str = Form(),
                        tax: Annotated[int, Form()] = None
                        ):
    return {"name": name, "description": description, "price": price, "tax": tax}

class UserInput(BaseModel):
    username: str
    email: str
    age: Optional[int] = None  # 나이는 선택 사항

    @classmethod
    def as_form(
        cls,
        username: str = Form(..., description="사용자 이름"),
        email: str = Form(..., description="이메일 주소"),
        age: Optional[int] = Form(None, description="나이 (선택)")
    ):
        return cls(username=username, email=email, age=age)

@app.post("/submit")
async def submit(user: UserInput = Depends(UserInput.as_form)):
    return {
        "message": f"User {user.username} submitted successfully!",
        "user_data": user.model_dump()
    }
