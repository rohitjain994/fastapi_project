from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.schemas import Item, ItemCreate, ItemUpdate
from app.exceptions import ResourceNotFoundException


router = APIRouter(prefix="/items", tags=["items"])


items_db = []
next_id = 1


@router.get("", response_model=List[Item])
async def get_items(
    name: Optional[str] = Query(None, min_length=1, max_length=100),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    is_available: Optional[bool] = Query(None),
    limit: Optional[int] = Query(None, ge=0, le=1000),
    offset: int = Query(0, ge=0),
):
    filtered_items = items_db
    if name is not None:
        filtered_items = [item for item in filtered_items if name.lower() in item["name"].lower()]
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] >= min_price]
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] <= max_price]
    if is_available is not None:
        filtered_items = [item for item in filtered_items if item["is_available"] == is_available]
    start = max(offset, 0)
    if limit is not None and limit >= 0:
        end = start + limit
        return filtered_items[start:end]
    return filtered_items[start:]


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise ResourceNotFoundException(name="Item", id=item_id)


@router.post("", response_model=Item)
async def create_item(item: ItemCreate):
    global next_id
    new_item = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_available": item.is_available,
    }
    items_db.append(new_item)
    next_id += 1
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemUpdate):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            update_data = item_update.dict(exclude_unset=True)
            items_db[i].update(update_data)
            return items_db[i]
    raise ResourceNotFoundException(name="Item", id=item_id)


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Item '{deleted_item['name']}' deleted successfully"}
    raise ResourceNotFoundException(name="Item", id=item_id)


