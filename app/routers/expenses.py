from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import Expense, User
from app.schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post(
    "",
    response_model=ExpenseResponse
)
def create_expense(

    expense: ExpenseCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    new_expense = Expense(

        title=expense.title,

        amount=expense.amount,

        category=expense.category,

        description=expense.description,

        date=expense.date,

        owner_id=current_user.id

    )

    db.add(new_expense)

    db.commit()

    db.refresh(new_expense)

    return new_expense

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(

    expense_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    expense = db.query(Expense).filter(

        Expense.id == expense_id,

        Expense.owner_id == current_user.id

    ).first()

    if expense is None:

        raise HTTPException(

            status_code=404,

            detail="Expense not found"

        )

    return expense

@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense(

    expense_id: int,

    updated: ExpenseUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    expense = db.query(Expense).filter(

        Expense.id == expense_id,

        Expense.owner_id == current_user.id

    ).first()

    if expense is None:

        raise HTTPException(

            status_code=404,

            detail="Expense not found"

        )

    for key, value in updated.model_dump(exclude_unset=True).items():

        setattr(expense, key, value)

    db.commit()

    db.refresh(expense)

    return expense

@router.delete("/{expense_id}")
def delete_expense(

    expense_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    expense = db.query(Expense).filter(

        Expense.id == expense_id,

        Expense.owner_id == current_user.id

    ).first()

    if expense is None:

        raise HTTPException(

            status_code=404,

            detail="Expense not found"

        )

    db.delete(expense)

    db.commit()

    return {

        "message":"Expense deleted successfully"
    }