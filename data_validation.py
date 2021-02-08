from durable.engine import MessageNotHandledException, MessageObservedException
from fastapi import FastAPI
from pydantic import BaseModel
from durable.lang import *
import json
import random
from datetime import date, datetime

app = FastAPI()


class DataSource(BaseModel):
    id: int
    data_source_id: int
    name: str
    row_count: int
    effective_date: date
    expiration_date: date


@app.post("/evaluate/{ruleset}")
async def evaluate(ruleset: str, fact: DataSource):
    # Cast from Fact -> JSON -> Dict
    f = json.loads(fact.json())
    try:
        # Using post() instead of assert_fact() avoids throwing an error when similar data in the object matches
        result = post(ruleset, f)
    except MessageNotHandledException as ex:
        print("Event matched no rules: {0}".format(ex.message))
        result = {"result": "Data passed validation ruleset '{0}'".format(ruleset)}
        print(result)
    except MessageObservedException as ex:
        print("Message has already been observed: {0}".format(ex.message))
        result = {"result": "Data may have passed validation, but validation states that fact was already evaluated."}
    return result


with ruleset('data_sources'):
    @when_all((m.data_source_id == 1) & (m.row_count < 100))  # Sample Data Source... each would be mapped independently
    def warn_below_minimum_record_count(c):
        result = {"result": "WARNING: {0} - Minimum row_count is 100. Received {1}...".format(c.m.name, c.m.row_count)}
        print(result)
        return result


    @when_any((m.row_count > 0) & (m.row_count < 50))
    def error_below_minimum_record_count(c):
        result = {
            "result": "ERROR: {0} - Minimum row count is below hard limit of 50 records! Received {1}".format(c.m.name,
                                                                                                              c.m.row_count)}
        print(result)
        return result

with ruleset('data_missing'):
    @when_all(m.data_source_id == 1)
    def warn_empty_row_count(c):
        result = {"result": "ERROR: {0} - row_count is a required field. Received {1}".format(c.m.name, c.m.row_count)}
        print(result)
        return result

with ruleset('data_bad_dates'):
    @when_all((m.effective_date > m.expiration_date) or (m.effective_date < datetime.now()))
    def error_invalid_date(c):
        result = {"result": "ERROR: {0} - effective_date > expiration date or effective_date is before {1}".format(c.m.name, datetime.now())}
