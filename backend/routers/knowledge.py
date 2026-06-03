from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from database import get_db
from models import KnowledgeBase
from schemas import KnowledgeBaseCreate, KnowledgeBaseUpdate, KnowledgeBaseResponse

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


@router.get("/", response_model=List[KnowledgeBaseResponse])
async def get_knowledge(
        category: Optional[str] = None,
        project_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
):
    query = select(KnowledgeBase)

    if category:
        query = query.where(KnowledgeBase.category == category)
    if project_id:
        query = query.where(KnowledgeBase.project_id == project_id)

    result = await db.execute(query)
    knowledge = result.scalars().all()
    return knowledge


@router.get("/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge_item(kb_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id))
    kb = result.scalar_one_or_none()
    if not kb:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return kb


@router.post("/", response_model=KnowledgeBaseResponse)
async def create_knowledge(kb: KnowledgeBaseCreate, db: AsyncSession = Depends(get_db)):
    db_kb = KnowledgeBase(**kb.model_dump())
    db.add(db_kb)
    await db.commit()
    await db.refresh(db_kb)
    return db_kb


@router.put("/{kb_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge(
        kb_id: int,
        kb: KnowledgeBaseUpdate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id))
    db_kb = result.scalar_one_or_none()
    if not db_kb:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    update_data = kb.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_kb, key, value)

    await db.commit()
    await db.refresh(db_kb)
    return db_kb


@router.delete("/{kb_id}")
async def delete_knowledge(kb_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(KnowledgeBase).where(KnowledgeBase.id == kb_id))
    db_kb = result.scalar_one_or_none()
    if not db_kb:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    await db.delete(db_kb)
    await db.commit()
    return {"detail": "Запись удалена"}


@router.get("/search/{query}", response_model=List[KnowledgeBaseResponse])
async def search_knowledge(query: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(KnowledgeBase).where(
            KnowledgeBase.question.ilike(f"%{query}%")
        )
    )
    knowledge = result.scalars().all()
    return knowledge