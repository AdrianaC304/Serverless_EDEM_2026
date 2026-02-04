from fastapi import FastAPI
from google.cloud import bigquery
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API de Usuarios")
client = bigquery.Client()

class User(BaseModel):
    user_id: str

@app.get("/users", response_model=List[User])
def get_users():
    query = """
        SELECT User_ID
        FROM `<PROJECT_ID>.<DATASET>.<TABLE_NAME_CLIENTS>`
        ORDER BY User_ID
        LIMIT 1000
    """
    query_job = client.query(query)
    results = query_job.result()

    users = []
    for row in results:
        users.append(User(user_id=row.User_ID))
    return users
