from typing import List

from ..models.account import Account, AccountResponse, AccountsResponse, CreateAccount
from ..utils import parse_response


class AccountsClient:
    """
    API methods related to Accounts.
    """

    def __init__(self, client, async_mode: bool = False):
        self.client = client
        self.async_mode = async_mode

    # --------------------
    # Asynchronous methods
    # --------------------

    async def get_accounts(self, budget_id: str) -> List[Account]:
        """
        Asynchronously retrieves all accounts for a budget.

        Args:
            budget_id (str): The ID of the budget.

        Returns:
            List[Account]: A list of accounts.
        """
        if not self.async_mode:
            raise RuntimeError("Client is not in async mode; use 'get_accounts_sync' instead")

        url = f"/budgets/{budget_id}/accounts"
        response = await self.client.get(url)
        data = parse_response(response, AccountsResponse)
        return data.accounts

    async def get_account(self, budget_id: str, account_id: str) -> Account:
        """
        Asynchronously retrieves a single account by ID.

        Args:
            budget_id (str): The ID of the budget.
            account_id (str): The ID of the account.

        Returns:
            Account: The account details.
        """
        if not self.async_mode:
            raise RuntimeError("Client is not in async mode; use 'get_account_sync' instead")

        url = f"/budgets/{budget_id}/accounts/{account_id}"
        response = await self.client.get(url)
        data = parse_response(response, AccountResponse)
        return data.account

    async def create_account(self, budget_id: str, account: CreateAccount) -> Account:
        """
        Asynchronously creates a new account.

        Args:
            budget_id (str): The ID of the budget.
            account (CreateAccount): The account data to create.

        Returns:
            Account: The created account.
        """
        if not self.async_mode:
            raise RuntimeError("Client is not in async mode; use 'create_account_sync' instead")

        url = f"/budgets/{budget_id}/accounts"
        payload = {"account": account.dict(exclude_unset=True)}
        response = await self.client.post(url, json=payload)
        data = parse_response(response, AccountResponse)
        return data.account

    # --------------------
    # Synchronous methods
    # --------------------

    def get_accounts_sync(self, budget_id: str) -> List[Account]:
        """
        Retrieves all accounts for a budget.

        Args:
            budget_id (str): The ID of the budget.

        Returns:
            List[Account]: A list of accounts.
        """
        if self.async_mode:
            raise RuntimeError("Client is in async mode; use 'get_accounts' instead")

        url = f"/budgets/{budget_id}/accounts"
        response = self.client.get(url)
        data = parse_response(response, AccountsResponse)
        return data.accounts

    def get_account_sync(self, budget_id: str, account_id: str) -> Account:
        """
        Retrieves a single account by ID.

        Args:
            budget_id (str): The ID of the budget.
            account_id (str): The ID of the account.

        Returns:
            Account: The account details.
        """
        if self.async_mode:
            raise RuntimeError("Client is in async mode; use 'get_account' instead")

        url = f"/budgets/{budget_id}/accounts/{account_id}"
        response = self.client.get(url)
        data = parse_response(response, AccountResponse)
        return data.account

    def create_account_sync(self, budget_id: str, account: CreateAccount) -> Account:
        """
        Creates a new account.

        Args:
            budget_id (str): The ID of the budget.
            account (CreateAccount): The account data to create.

        Returns:
            Account: The created account.
        """
        if self.async_mode:
            raise RuntimeError("Client is in async mode; use 'create_account' instead")

        url = f"/budgets/{budget_id}/accounts"
        payload = {"account": account.dict(exclude_unset=True)}
        response = self.client.post(url, json=payload)
        data = parse_response(response, AccountResponse)
        return data.account
