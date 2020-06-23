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


@app.post("/evaluate")
async def evaluate(fact: Fact):
    # Cast from Fact -> JSON -> Dict
    f = json.loads(fact.json())
    result = assert_fact('test', f)
    return result


with ruleset('test'):
    @when_all(m.subject.matches('3[4-7][0-9]{13}'))
    def amex(c):
        result = {"result": "Amex Detected {0}".format(c.m.subject)}
        print(result)
        return result

    @when_all(m.subject.matches('4[0-9]{12}([0-9]{3})?'))
    def visa(c):
        result = {"result": "Visa Detected {0}".format(c.m.subject)}
        print(result)
        return result

    @when_all(m.subject.matches('(5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|2720)[0-9]{12}'))
    def mastercard(c):
        result = {"result": "Mastercard Detected {0}".format(c.m.subject)}
        print(result)
        return result

# assert_fact('test', {'subject': '375678956789765'})
# assert_fact('test', {'subject': '4345634566789888'})
# assert_fact('test', {'subject': '2228345634567898'})
