from fastapi import Request, Depends
from libs.ynab.ynab_client import YNABClient

def get_ynab_client(request: Request) -> YNABClient:
    """
    Dependency to retrieve the YNABClient from the application state.
    """
    return request.app.state.ynab_client
