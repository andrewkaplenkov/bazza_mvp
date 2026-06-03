from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from database import get_db
from models import PartnerReward
from schemas import PartnerRewardCreate, PartnerRewardUpdate, PartnerRewardResponse

router = APIRouter(prefix="/rewards", tags=["Partner Rewards"])


@router.get("/", response_model=List[PartnerRewardResponse])
async def get_rewards(
        project_id: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
):
    query = select(PartnerReward)
    if project_id:
        query = query.where(PartnerReward.project_id == project_id)

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=PartnerRewardResponse)
async def create_reward(reward: PartnerRewardCreate, db: AsyncSession = Depends(get_db)):
    db_reward = PartnerReward(**reward.model_dump())
    db.add(db_reward)
    await db.commit()
    await db.refresh(db_reward)
    return db_reward


@router.put("/{reward_id}", response_model=PartnerRewardResponse)
async def update_reward(
        reward_id: int,
        reward: PartnerRewardUpdate,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(PartnerReward).where(PartnerReward.id == reward_id))
    db_reward = result.scalar_one_or_none()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Вознаграждение не найдено")

    update_data = reward.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_reward, key, value)

    await db.commit()
    await db.refresh(db_reward)
    return db_reward


@router.delete("/{reward_id}")
async def delete_reward(reward_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PartnerReward).where(PartnerReward.id == reward_id))
    db_reward = result.scalar_one_or_none()
    if not db_reward:
        raise HTTPException(status_code=404, detail="Вознаграждение не найдено")

    await db.delete(db_reward)
    await db.commit()
    return {"detail": "Вознаграждение удалено"}