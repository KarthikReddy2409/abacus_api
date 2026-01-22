import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import storage


app = FastAPI(title="Abacus Service")


def get_node_id():
    return os.getenv("NODE_ID", "unknown")


class NumberInput(BaseModel):
    number: float


class SumResponse(BaseModel):
    sum: float
    node: str = ""


class AddResponse(BaseModel):
    added: float
    new_sum: float
    node: str = ""

class ResetResponse(BaseModel):
    message: str = "sum reset to zero"
    node: str = ""


@app.get("/health")
def health_check():
    return {"status": "ok", "node": get_node_id()}


@app.post("/abacus/number", response_model=AddResponse)
def add_number(data: NumberInput):
    # TODO: maybe add rate limiting here later
    new_sum = storage.add_to_sum(data.number)
    return AddResponse(added=data.number, new_sum=new_sum, node=get_node_id())


@app.get("/abacus/sum", response_model=SumResponse)
def get_current_sum():
    try:
        return SumResponse(sum=storage.get_sum(), node=get_node_id())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/abacus/sum", response_model=ResetResponse)
def reset_sum():
    try:
        storage.reset_sum()
        return ResetResponse(node=get_node_id())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
