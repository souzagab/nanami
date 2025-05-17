from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.types.enums import AccountMappingStatus, AccountMappingType
from app.schemas.account_mapping import (
  AccountMappingCreate,
  AccountMappingUpdate,
)
from app.services.account_mapping_service import AccountMappingService, get_account_mapping_service

router = APIRouter(prefix="/mappings", tags=["account_mappings"])
templates = Jinja2Templates(directory="app/templates")


# Dependency function to parse AccountMappingCreate from form data
async def get_mapping_create_form(
  name: str = Form(...),
  account_type: AccountMappingType = Form(...),
  pluggy_item_id: str = Form(...),
  pluggy_account_id: str = Form(...),
  ynab_account_id: str = Form(...),
  status: AccountMappingStatus = Form(AccountMappingStatus.ACTIVE),
) -> AccountMappingCreate:
  return AccountMappingCreate(
    name=name,
    account_type=account_type,
    pluggy_item_id=pluggy_item_id,
    pluggy_account_id=pluggy_account_id,
    ynab_account_id=ynab_account_id,
    status=status,
  )


# Dependency function to parse AccountMappingUpdate from form data
async def get_mapping_update_form(
  name: str | None = Form(None),
  account_type: AccountMappingType | None = Form(None),
  pluggy_item_id: str | None = Form(None),
  pluggy_account_id: str | None = Form(None),
  ynab_account_id: str | None = Form(None),
  status: AccountMappingStatus | None = Form(None),
) -> AccountMappingUpdate:
  return AccountMappingUpdate(
    name=name,
    account_type=account_type,
    pluggy_item_id=pluggy_item_id,
    pluggy_account_id=pluggy_account_id,
    ynab_account_id=ynab_account_id,
    status=status,
  )


@router.get("/", response_class=HTMLResponse, name="list_account_mappings")
async def list_account_mappings(
  request: Request, service: Annotated[AccountMappingService, Depends(get_account_mapping_service)]
):
  """
  Display a list of all account mappings.
  """
  mappings = await service.get_all_mappings()
  return templates.TemplateResponse(
    "account_mappings/list.html",
    {
      "request": request,
      "mappings": mappings,
      "account_mapping_types": AccountMappingType,
      "account_mapping_status": AccountMappingStatus,
    },
  )


@router.get("/new", response_class=HTMLResponse, name="new_account_mapping_form")
async def new_account_mapping_form(request: Request):
  """
  Display a form to create a new account mapping.
  """
  return templates.TemplateResponse(
    "account_mappings/create.html",
    {"request": request, "account_mapping_types": AccountMappingType, "account_mapping_status": AccountMappingStatus},
  )


@router.post("/", status_code=201, name="create_account_mapping")
async def create_account_mapping(
  mapping_in: Annotated[AccountMappingCreate, Depends(get_mapping_create_form)],
  service: Annotated[AccountMappingService, Depends(get_account_mapping_service)],
):
  """
  Create a new account mapping.
  """
  await service.create_mapping(mapping_in)
  return RedirectResponse(url=router.url_path_for("list_account_mappings"), status_code=303)


@router.get("/{mapping_id}/edit", response_class=HTMLResponse, name="edit_account_mapping_form")
async def edit_account_mapping_form(
  request: Request, mapping_id: UUID, service: Annotated[AccountMappingService, Depends(get_account_mapping_service)]
):
  """
  Display a form to edit an existing account mapping.
  """
  mapping = await service.get_mapping_by_id(mapping_id)
  if not mapping:
    raise HTTPException(status_code=404, detail="Account mapping not found")
  return templates.TemplateResponse(
    "account_mappings/edit.html",
    {
      "request": request,
      "mapping": mapping,
      "account_mapping_types": AccountMappingType,
      "account_mapping_status": AccountMappingStatus,
    },
  )


@router.post("/{mapping_id}", name="update_account_mapping")
async def update_account_mapping(
  mapping_id: UUID,
  mapping_in: Annotated[AccountMappingUpdate, Depends(get_mapping_update_form)],
  service: Annotated[AccountMappingService, Depends(get_account_mapping_service)],
):
  """
  Update an existing account mapping.
  """
  updated_mapping = await service.update_mapping(mapping_id, mapping_in)
  if not updated_mapping:
    raise HTTPException(status_code=404, detail="Account mapping not found")
  return RedirectResponse(url=router.url_path_for("list_account_mappings"), status_code=303)


@router.get("/{mapping_id}/delete", name="delete_account_mapping")
async def delete_account_mapping(
  mapping_id: UUID, service: Annotated[AccountMappingService, Depends(get_account_mapping_service)]
):
  """
  Delete an account mapping.
  """
  deleted_mapping = await service.delete_mapping(mapping_id)
  if not deleted_mapping:
    raise HTTPException(status_code=404, detail="Account mapping not found")
  return RedirectResponse(url=router.url_path_for("list_account_mappings"), status_code=303)
