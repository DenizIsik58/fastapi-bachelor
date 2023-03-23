import dotenv
import uvicorn
from fastapi import FastAPI
from routers import login, products, register,authentication

api = FastAPI()

api.include_router(login.login_router)
api.include_router(products.products_router, prefix="/products")
api.include_router(register.register_router, prefix="/register")
api.include_router(authentication.authentication_router, prefix="/")

@api.get("/")
async def root():
    return {"message": "Welcome to the best api!"}


@api.on_event("startup")
async def startup_event():
    dotenv.load_dotenv()


if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, log_level="info", reload=True)
