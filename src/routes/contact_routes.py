from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import contact_def as repositories_contact
from src.schemas.contact_schema import ContactsResponse, ContactCreate, ContactUpdate


router = APIRouter(prefix='/contacts', tags=['contacts'])

@router.get("/search/{query}", response_model=List[ContactsResponse])
async def get_contact_query(query: str, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.get_contact_query(query, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

# Функція для отримання контактів з днями народження на найближчі 7 днів
@router.get("/api/contacts/birthdays", response_model=List[ContactsResponse])
async def get_birthdays_next_week(days: int = Query(7), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.get_birthdays_next_week(days, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact

@router.get("/", response_model=List[ContactsResponse])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                           db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contact.get_all_contacts(limit, offset, db)
    return contacts






@router.get("/{contact_id}", response_model=ContactsResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact




@router.post("/", response_model=ContactsResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactsResponse)
async def update_contact(body: ContactUpdate, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contact.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return None
