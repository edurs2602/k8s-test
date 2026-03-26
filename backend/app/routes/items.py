from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ItemCreate, ItemList, ItemResponse, ItemUpdate
from app.services import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    item_data: ItemCreate,
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    return await ItemService.create(db, item_data)


@router.get("/", response_model=ItemList)
async def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    active_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
) -> ItemList:
    items, total = await ItemService.get_list(db, page, page_size, active_only)
    return ItemList(
        items=[ItemResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    item = await ItemService.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: AsyncSession = Depends(get_db),
) -> ItemResponse:
    item = await ItemService.update(db, item_id, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse.model_validate(item)


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    success = await ItemService.delete(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")