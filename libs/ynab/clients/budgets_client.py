from typing import List, Optional

from ..models.budget import (
    BudgetDetail,
    BudgetResponse,
    BudgetSettings,
    BudgetSettingsResponse,
    BudgetsResponse,
    BudgetSummary,
)
from ..utils import parse_response


class BudgetsClient:
    """
    API methods related to Budgets.
    """

    def __init__(self, client, async_mode: bool = False):
        self.client = client
        self.async_mode = async_mode

    # --------------------
    # Asynchronous methods
    # --------------------

    async def get_budgets(self, include_accounts: bool = False) -> List[BudgetSummary]:
        """
        Asynchronously retrieves a list of budgets.

        Args:
            include_accounts (bool): Whether to include list of accounts for each budget.

        Returns:
            List[BudgetSummary]: A list of budget summaries.
        """
        if not self.async_mode:
            raise RuntimeError("Client is not in async mode; use 'get_budgets_sync' instead")

        params = {'include_accounts': str(include_accounts).lower()}
        response = await self.client.get('/budgets', params=params)
        data = parse_response(response, BudgetsResponse)
        return data.budgets

    async def get_budget(self, budget_id: str, last_knowledge_of_server: Optional[int] = None) -> BudgetDetail:
        """
        Asynchronously retrieves a single budget by ID.

        Args:
            budget_id (str): The ID of the budget.
            last_knowledge_of_server (Optional[int]): The starting server knowledge.

        Returns:
            BudgetDetail: Detailed budget information.
        """
        if not self.async_mode:
            raise RuntimeError("Client is not in async mode; use 'get_budget_sync' instead")

        params = {}
        if last_knowledge_of_server is not None:
            params['last_knowledge_of_server'] = last_knowledge_of_server

        response = await self.client.get(f'/budgets/{budget_id}', params=params)
        data = parse_response(response, BudgetResponse)
        return data.budget

    async def get_budget_settings(self, budget_id: str) -> BudgetSettings:
        """
        Asynchronously retrieves settings for a budget.

        Args:
            budget_id (str): The ID of the budget.

        Returns:
            BudgetSettings: The settings of the budget.
        """
        if not self.async_mode:
            raise RuntimeError("Client is not in async mode; use 'get_budget_settings_sync' instead")

        response = await self.client.get(f'/budgets/{budget_id}/settings')
        data = parse_response(response, BudgetSettingsResponse)
        return data.settings

    # --------------------
    # Synchronous methods
    # --------------------

    def get_budgets_sync(self, include_accounts: bool = False) -> List[BudgetSummary]:
        """
        Retrieves a list of budgets.

        Args:
            include_accounts (bool): Whether to include list of accounts for each budget.

        Returns:
            List[BudgetSummary]: A list of budget summaries.
        """
        if self.async_mode:
            raise RuntimeError("Client is in async mode; use 'get_budgets' instead")

        params = {'include_accounts': str(include_accounts).lower()}
        response = self.client.get('/budgets', params=params)
        data = parse_response(response, BudgetsResponse)
        return data.budgets

    def get_budget_sync(self, budget_id: str, last_knowledge_of_server: Optional[int] = None) -> BudgetDetail:
        """
        Retrieves a single budget by ID.

        Args:
            budget_id (str): The ID of the budget.
            last_knowledge_of_server (Optional[int]): The starting server knowledge.

        Returns:
            BudgetDetail: Detailed budget information.
        """
        if self.async_mode:
            raise RuntimeError("Client is in async mode; use 'get_budget' instead")

        params = {}
        if last_knowledge_of_server is not None:
            params['last_knowledge_of_server'] = last_knowledge_of_server

        response = self.client.get(f'/budgets/{budget_id}', params=params)
        data = parse_response(response, BudgetResponse)
        return data.budget

    def get_budget_settings_sync(self, budget_id: str) -> BudgetSettings:
        """
        Retrieves settings for a budget.

        Args:
            budget_id (str): The ID of the budget.

        Returns:
            BudgetSettings: The settings of the budget.
        """
        if self.async_mode:
            raise RuntimeError("Client is in async mode; use 'get_budget_settings' instead")

        response = self.client.get(f'/budgets/{budget_id}/settings')
        data = parse_response(response, BudgetSettingsResponse)
        return data.settings
