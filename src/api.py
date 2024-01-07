import logging_settings
from strategies import strategies

from fastapi import FastAPI, Body

import logging
from decimal import Decimal


logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/strategies")
def get_strategies():
    return [strategy.name for strategy in strategies.values()]
