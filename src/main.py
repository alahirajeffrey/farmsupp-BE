from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from article.router import router as article_router
from auth.router import router as auth_router
from profile.router import router as profile_router
from chat.router import router as chat_router
from product.router import router as product_router
from other.router import router as other_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(profile_router , prefix="/api/v1/profile", tags=["profile"])
app.include_router(article_router , prefix="/api/v1/article", tags=["article"])
app.include_router(chat_router , prefix="/api/v1/chat", tags=["chat"])
app.include_router(product_router , prefix="/api/v1/product", tags=["product"])
app.include_router(other_router , prefix="/api/v1/other", tags=["other"])


@app.get("/")
async def root():
    return {"message": "Server running"}