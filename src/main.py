from typing import Union
from fastapi import FastAPI

app = FastAPI()
 
import debugpy
debugpy.listen(("0.0.0.0", 5678))

@app.get("/")
def read_root():
    return {"Hello": "World1 ass wiper"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
