from fastapi import FastAPI, Request

app = FastAPI()
# 요청(Request) 객체를 통해 요청한 클라이언트의 ip 정보, 요청 헤더, 쿼리스트링, 요청한 전체 url, http 메서드(get)

# http://127.0.0.1:8081/items?item_code=8
@app.get("/items")
async def read_item(request: Request):
    client_host = request.client.host
    headers = request.headers
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method
    
    return {
            "client_host": client_host,
            "headers": headers,
            "query_params": query_params,
            "path_params": path_params,
            "url": str(url),
            "http_method":  http_method
        }

# http://127.0.0.1:8081/items/34
@app.get("/items/{item_group}")
async def read_item_p(request: Request, item_group: str):
    client_host = request.client.host
    headers = request.headers 
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method":  http_method
    }

# SwaggerUI에서 테스트가 안되므로 테스트는 Thunder Client로 진행

@app.post("/items_json/")
async def create_item_json(request: Request):
    data =  await request.json()  # Parse JSON body
    print("received_data:", data)
    return {"received_data": data}

# SwaggerUI에서 테스트가 안되므로 테스트는 Thunder Client로 진행

@app.post("/items_form/")
async def create_item_form(request: Request):
    data = await request.form() # Parse Form body
    print("received_data:", data)
    return {"received_data": data}
