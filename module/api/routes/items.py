"""
Simple example of using FastAPI-MCP to add an MCP server to a FastAPI app.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional


# Create a simple FastAPI app
router = APIRouter()


# Define some models
class Item(BaseModel):
    id: int = Field(description="Unique identifier for the item")
    name: str = Field(description="Name of the item")
    description: Optional[str] = Field(None, description="Description of the item")
    price: float = Field(description="Price of the item")
    
    tag: Optional[str] = Field(None, description="Tag for the item")


# In-memory database
items_db: dict[int, Item] = {}


# Define some endpoints
@router.get("/items/", response_model=List[Item], tags=["items"], operation_id="list_items")
async def list_items(skip: int = 0, limit: int = 10):
    """
    List all items in the database.

    Returns a list of items, with pagination support.
    """
    return list(items_db.values())[skip : skip + limit]


@router.get("/items/{item_id}", response_model=Item, tags=["items"], operation_id="get_item")
async def read_item(item_id: int):
    """
    Get a specific item by its ID.

    Raises a 404 error if the item does not exist.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/items/", response_model=Item, tags=["items"], operation_id="create_item")
async def create_item(item: Item):
    """
    Create a new item in the database.

    Returns the created item with its assigned ID.
    """
    items_db[item.id] = item
    return item


@router.put("/items/{item_id}", response_model=Item, tags=["items"], operation_id="update_item")
async def update_item(item_id: int, item: Item):
    """
    Update an existing item.

    Raises a 404 error if the item does not exist.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    item.id = item_id
    items_db[item_id] = item
    return item


@router.delete("/items/{item_id}", tags=["items"], operation_id="delete_item")
async def delete_item(item_id: int):
    """
    Delete an item from the database.

    Raises a 404 error if the item does not exist.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"message": "Item deleted successfully"}


@router.get("/items/search/", response_model=List[Item], tags=["search"], operation_id="search_items")
async def search_items(
    q: Optional[str] = Query(None, description="Search query string"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    # tags: List[str] = Query([], description="Filter by tags"),
):
    """
    Search for items with various filters.

    Returns a list of items that match the search criteria.
    """
    results = list(items_db.values())

    # Filter by search query
    if q:
        q = q.lower()
        results = [
            item for item in results if q in item.name.lower() or (item.description and q in item.description.lower())
        ]

    # Filter by price range
    if min_price is not None:
        results = [item for item in results if item.price >= min_price]
    if max_price is not None:
        results = [item for item in results if item.price <= max_price]

    # # Filter by tags
    # if tags:
    #     results = [item for item in results if all(tag in item.tags for tag in tags)]

    return results


# Add sample data
sample_items = [
    Item(id=1, name="Hammer", description="A tool for hammering nails", price=9.99),
    Item(id=2, name="Screwdriver", description="A tool for driving screws", price=7.99),
    Item(id=3, name="Wrench", description="A tool for tightening bolts", price=12.99),
    Item(id=4, name="Saw", description="A tool for cutting wood", price=19.99),
    Item(id=5, name="Drill", description="A tool for drilling holes", price=49.99),
]
for item in sample_items:
    items_db[item.id] = item