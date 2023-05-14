import os
import dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect

from routers import login, products, authentication, register, reviews, purchase, logout

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(login.login_router, tags=["Authentication"])
api.include_router(reviews.reviews_router, tags=["Reviews"])
api.include_router(products.products_router, tags=["Products"])
api.include_router(register.register_router, tags=["Register"])
api.include_router(authentication.authentication_router, tags=["Authentication"])
api.include_router(purchase.purchase_router, tags=["Purchase history"])
api.include_router(logout.logout_router, tags=["Authentication"])

@api.get("/")
async def root():
    return {"message": "Welcome to the best api!"}

@api.on_event("startup")
async def startup_event():
    dotenv.load_dotenv()
    connect(host=os.getenv("CONNECTION_STRING"))


if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, log_level="info", reload=True)
