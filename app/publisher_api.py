from app.common.fastapi_app import get_app
from app.routers.auth import auth_router as auth_router
from app.routers.publisher import router as publisher_router
from app.routers.studios import router as studios_router

app = get_app()

app.include_router(auth_router, prefix="/auth")
app.include_router(studios_router, prefix="/studios")
app.include_router(publisher_router, prefix="/publisher")
