from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
N=10
# Initialize bloom filter array
bloomarr = [0] * N

# Hash functions
def hashf1(var: int) -> int:
    return (2 * var + 5) % N

def hashf2(var: int) -> int:
    return (var * 150 - 250) % N

# Add function
def add(var: int):
    bloomarr[hashf1(var)] = 1
    bloomarr[hashf2(var)] = 1

# Check function
def check(var: int) -> str:
    if bloomarr[hashf1(var)] == 1 and bloomarr[hashf2(var)] == 1:
        return f"{var} may be present"
    else:
        return f"{var} is not present probably"

# Pydantic models for input validation
class ValueInput(BaseModel):
    value: int

@app.post("/add/")
def add_value(input_data: ValueInput):
    add(input_data.value)
    return {"message": f"Value {input_data.value} added successfully"}

@app.get("/check/{value}")
def check_value(value: int):
    result = check(value)
    return {"message": result}

@app.get("/bloomarr")
def see_bloom():
    op = str()
    cnt = 0
    for var in bloomarr:
        cnt += 1
        if var == 1:
            op = op + f"Pos {cnt}; "
    return op
