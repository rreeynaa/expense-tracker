from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import SessionLocal, engine, Base
from models import Expense

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = SessionLocal()
    try:
        expenses = db.query(Expense).all()
        total = sum(expense.amount for expense in expenses)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "expenses": expenses,
                "total": total
            }
        )
    finally:
        db.close()


@app.post("/add")
def add_expense(
    title: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...)
):
    db = SessionLocal()
    try:
        expense = Expense(title=title, amount=amount, category=category)
        db.add(expense)
        db.commit()
    finally:
        db.close()
    return RedirectResponse(url="/", status_code=303)


@app.get("/delete/{expense_id}")
def delete_expense(expense_id: int):
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            db.delete(expense)
            db.commit()
    finally:
        db.close()
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/expenses")
def get_expenses():
    db = SessionLocal()
    try:
        expenses = db.query(Expense).all()
        return JSONResponse([
            {
                "id": e.id,
                "title": e.title,
                "amount": e.amount,
                "category": e.category
            }
            for e in expenses
        ])
    finally:
        db.close()