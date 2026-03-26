from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    @staticmethod
    async def create(db: AsyncSession, item_data: ItemCreate) -> Item:
        db_item = Item(**item_data.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int) -> Item | None:
        result = await db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        active_only: bool = False,
    ) -> tuple[list[Item], int]:
        query = select(Item)

        if active_only:
            query = query.where(Item.is_active == True)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        items = list(result.scalars().all())

        return items, total

    @staticmethod
    async def update(db: AsyncSession, item_id: int, item_data: ItemUpdate) -> Item | None:
        db_item = await ItemService.get_by_id(db, item_id)
        if not db_item:
            return None

        update_data = item_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def delete(db: AsyncSession, item_id: int) -> bool:
        db_item = await ItemService.get_by_id(db, item_id)
        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True