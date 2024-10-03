from fastapi import Request
from libs.pluggy.pluggy_client import PluggyAIClient
from libs.ynab.ynab_client import YNABClient


def get_ynab_client(request: Request) -> YNABClient:
    """
    Dependency to retrieve the YNABClient from the application state.
    """
    return request.app.state.ynab_client

def get_pluggy_client(request: Request) -> PluggyAIClient:
    return request.app.state.pluggy_client
