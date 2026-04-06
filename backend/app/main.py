from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Prep Track")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
progress=[{"id":1,"topic":"Arrays","solved":15,"total":20},{"id":2,"topic":"DP","solved":6,"total":15}]
tasks=[{"id":1,"title":"Solve 2 DP questions"},{"id":2,"title":"Revise SQL joins"}]
@app.get("/progress")
def get_progress(): return progress
@app.get("/tasks")
def get_tasks(): return tasks
