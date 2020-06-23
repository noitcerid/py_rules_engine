from fastapi import FastAPI
from pydantic import BaseModel
from durable.lang import *
import json

app = FastAPI()


class Fact(BaseModel):
    subject: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/evaluate/{ruleset}")
async def evaluate(ruleset: str, fact: Fact):
    # Cast from Fact -> JSON -> Dict
    f = json.loads(fact.json())
    result = assert_fact(ruleset, f)
    return result


with ruleset('missing_data'):
    @when_all(m.subject == '')
    def missing_subject(c):
        result = {"result": "Subject is empty. A value is required."}
        print(result)
        return result

