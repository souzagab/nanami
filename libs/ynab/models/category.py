from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Category(BaseModel):
    """
    Represents a category in a budget.
    """
    id: UUID = Field(..., description="The unique identifier of the category")
    category_group_id: UUID = Field(..., description="The unique identifier of the category group")
    name: str = Field(..., description="The name of the category")
    hidden: bool = Field(..., description="Whether the category is hidden")
    note: Optional[str] = Field(None, description="Notes about the category")
    budgeted: int = Field(..., description="Budgeted amount in milliunits")
    activity: int = Field(..., description="Activity amount in milliunits")
    balance: int = Field(..., description="Balance in milliunits")
    deleted: bool = Field(..., description="Whether the category has been deleted")



class CategoryGroup(BaseModel):
    """
    Represents a category group in a budget.
    """
    id: UUID = Field(..., description="The unique identifier of the category group")
    name: str = Field(..., description="The name of the category group")
    hidden: bool = Field(..., description="Whether the category group is hidden")
    deleted: bool = Field(..., description="Whether the category group has been deleted")
    categories: List[Category] = Field(..., description="The list of categories in the group")


