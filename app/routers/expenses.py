from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
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

#===========================================
##CRUD ENDPOINTS FOR EXPENSES
#===========================================

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


@router.get("", response_model=list[ExpenseResponse])
def get_expenses(
    category: str | None = Query(None, description="Filter by category"),
    search: str | None = Query(None, description="Search by expense title"),
    sort_by: str = Query("date", description="Sort order: asc or desc"),
    order: str = Query("desc", description="Sort order: asc or desc"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return"),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = db.query(Expense).filter(
        Expense.owner_id == current_user.id
    )

    # Category filter
    if category:
        query = query.filter(Expense.category == category)

    # Search in title
    if search:
        query = query.filter(
            Expense.title.ilike(f"%{search}%")
        )

    # Sorting
    sortable_fields = {
        "date": Expense.date,
        "amount": Expense.amount,
        "title": Expense.title,
        "category": Expense.category
    }

    #If someone enters: GET /expenses?sort_by=random, you silently sort by date.
    if sort_by not in sortable_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by. Choose from {list(sortable_fields.keys())}"
        )

    sort_column = sortable_fields[sort_by]

    if order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    elif order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        raise HTTPException(
            status_code=400,
            detail="Order must be 'asc' or 'desc'"
        )

    # Pagination
    expenses = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return expenses


#===========================================
##EXPENSE SUMMARY ENDPOINTS
#===========================================

@router.get("/summary")
def expense_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    summary = db.query(
        func.sum(Expense.amount).label("total_expenses"),
        func.count(Expense.id).label("total_transactions"),
        func.max(Expense.amount).label("highest_expense"),
        func.avg(Expense.amount).label("average_expense")
    ).filter(
        Expense.owner_id == current_user.id
    ).first()

    return {
        "total_expenses": summary.total_expenses or 0,
        "total_transactions": summary.total_transactions,
        "highest_expense": summary.highest_expense or 0,
        "average_expense": round(summary.average_expense or 0, 2)
    }

#######


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

