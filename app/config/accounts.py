import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

# Workaround to have Items available since Pluggy.ai API don't have a list endpoint.

class PluggyAccountRef(str, Enum):
  E_NUBANK = os.getenv("E_NUBANK_ITEM_ID")
  E_SICOOB = os.getenv("E_SICOOB_ITEM_ID")
  SANTANDER = os.getenv("SANTANDER_ITEM_ID")
  SICOOB = os.getenv("SICOOB_ITEM_ID")
  NUBANK = os.getenv("NUBANK_ITEM_ID")
  # CAIXA = os.getenv("CAIXA_ITEM_ID")