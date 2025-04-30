# Pydantic 모델 정의 및 ValidationError 예외 처리용 모듈
from pydantic import BaseModel, ValidationError

# 타입 힌트를 위한 도구들 (선택적 필드 정의를 위한 Optional 포함)
from typing import List, Optional

# JSON 문자열 파싱을 위한 표준 모듈
import json


# -------------------------
# ✅ Pydantic 모델 정의
# -------------------------
class User(BaseModel):
    id: int  # 정수형 ID (필수)
    name: str  # 사용자 이름 (필수)
    email: str  # 이메일 (필수)
    age: int | None = None  # 선택적 필드 (기본값 None)

    # age는 Optional[int] = None 도 가능 (Python 3.10 이상에서는 int | None 문법 허용됨)


# -------------------------
# ❌ 일반 Python 클래스 정의
# -------------------------
class UserClass:
    def __init__(self, id: int, name: str, email: str, age: int):
        # 타입 체크 없음, 단순 할당
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        # 일부 필드만 출력하는 사용자 정의 메서드
        return f"id: {self.id}, name: {self.name}"

    def __str__(self):
        # 객체를 print()로 출력할 때 호출됨 (문자열 표현)
        return f"id: {self.id}, name: {self.name}, email: {self.email}, age: {self.age}"


# -------------------------
# 일반 클래스 객체 생성
# -------------------------
userobj = UserClass(10, 'test_name', 'tname@example.com', 40)
print("userobj:", userobj, userobj.id)  # __str__ 오버라이드 덕분에 사람이 읽기 좋은 문자열 출력됨


# -------------------------
# Pydantic 모델 객체 생성
# -------------------------
user = User(id=10, name="test_name", email="tname@example.com", age=40)
print("user:", user, user.id)  # Pydantic 객체는 자동으로 타입 체크 및 문서화 구조 유지


# -------------------------
# dict 언패킹을 통한 모델 생성 (** 연산자 사용)
# -------------------------
user_from_dict = User(**{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40})
print("user_from_dict:", user_from_dict, user_from_dict.id)


# -------------------------
# JSON 문자열 → dict → Pydantic 모델 생성
# -------------------------
json_string = '{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40}'
json_dict = json.loads(json_string)  # 문자열을 Python dict로 변환
user_from_json = User(**json_dict)  # 변환된 dict를 모델에 전달
print("user_from_json:", user_from_json, user_from_json.id)


# -------------------------
# Pydantic 모델 상속 (필드 확장)
# -------------------------
class AdvancedUser(User):
    advanced_level: int  # 추가 필드 정의

# 생성 시 순서대로 값을 넣으면 안 되고, 키워드 인자로 명시해야 함
adv_user = AdvancedUser(id=10, name="test_name", email="tname@example.com", age=40, advanced_level=9)
print("adv_user:", adv_user)


# -------------------------
# Nested 모델 정의 (중첩된 JSON 구조 대응)
# -------------------------
class Address(BaseModel):
    street: str
    city: str

class UserNested(BaseModel):
    name: str
    age: int
    address: Address  # 중첩된 Pydantic 모델 필드

# -------------------------
# 중첩 JSON 문자열 → Pydantic 모델
# -------------------------

# JSON 형식의 문자열 데이터 (Nested 구조)
# → 사용자 정보(name, age)와 주소 정보(address)가 포함됨
# → address는 다시 street, city라는 하위 필드를 가지는 중첩된 구조임
json_string_nested = '{"name": "John Doe", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}}'

# json.loads() 함수는 JSON 문자열을 Python의 dict 자료형으로 변환함
# 즉 json_string_nested → Python dict 객체로 바뀜
json_dict_nested = json.loads(json_string_nested)

# Pydantic 모델(UserNested)에 **dict를 언패킹(**)해서 전달**
# 내부적으로 다음이 자동으로 수행됨:
# - name, age는 기본 필드로 바로 매핑
# - address는 dict 타입이지만, UserNested 모델에서 Address라는 Pydantic 모델로 선언되어 있으므로
#   Pydantic이 알아서 Address 객체로 변환해줌 (자동 중첩 파싱)
user_nested_01 = UserNested(**json_dict_nested)

# 출력:
# - 전체 모델 객체 출력
# - 중첩된 address 객체 출력
# - address 내부의 city 필드에 직접 접근
print("user_nested_01:", user_nested_01, user_nested_01.address, user_nested_01.address.city)
# 예시 출력:
# user_nested_01: name='John Doe' age=30 address=Address(street='123 Main St', city='Anytown') 
# Address(street='123 Main St', city='Anytown') 
# Anytown



# -------------------------
# dict 직접 전달로 중첩 객체 생성
# -------------------------
user_nested_02 = UserNested(
    name="test_name",
    age=40,
    address={"street": "123 Main St", "city": "Anytown"}  # 내부 dict도 자동 Address 객체로 변환
)
print("user_nested_02:", user_nested_02, user_nested_02.address, user_nested_02.address.city)


# -------------------------
# Pydantic 모델 → Python dict로 직렬화 (Serialization)
# -------------------------
user_dump_01 = user.model_dump()
print(user_dump_01, type(user_dump_01))  # dict 타입 → JSON 응답 만들 때 자주 사용


# -------------------------
# Pydantic 모델 → JSON 문자열로 직렬화
# -------------------------
user_dump_02 = user.model_dump_json()
print(user_dump_02, type(user_dump_02))  # str 타입 (JSON 형식)
