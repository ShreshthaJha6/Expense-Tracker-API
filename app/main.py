from fastapi import FastAPI

from app.database import engine
from app.models import Base

from app.routers.auth import router as auth_router
from app.routers.expenses import router as expense_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API"
)

app.include_router(auth_router)
app.include_router(expense_router)


@app.get("/")
def home():
    return {
        "message": "Expense Tracker API"
    }