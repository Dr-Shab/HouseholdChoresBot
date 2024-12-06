from fastapi import FastAPI, status
import datahandler
import uvicorn
from pydantic import BaseModel

class TokenRequest(BaseModel):
    token: str

class RotateRequest(BaseModel):
    category: str


app = FastAPI()

workers, tokens, aemtli, entsorgen = datahandler.getem()

@app.get("/api/get_em")
def get_config():
    return workers, tokens, aemtli, entsorgen

@app.get("/api/store_em")
def store_them():
    storing = datahandler.storethem(workers, tokens, aemtli, entsorgen)
    if not storing:
        return status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        return status.HTTP_200_OK

@app.get("/api/wiki_how")
def get_wiki_links():
    wiki_aemtli = datahandler.aemtli_cleaner(aemtli)
    wiki_links = {}

    for idx, amt in enumerate(wiki_aemtli):
        links = datahandler.wiki_how_help_links(amt)
        wiki_links[aemtli[idx]] = links

    return wiki_links

@app.post("/api/rotate_list")
def rotate_list(request: RotateRequest):
    if request.category == "workers":
        datahandler.rotateList(workers)
    elif request.category == "entsorgen":
        datahandler.rotateList(entsorgen)

@app.post("/api/get_token_link")
def generate_token_link(request: TokenRequest):
    token = request.token
    link = datahandler.generate_link(token)
    return link

@app.get("/api/store_tokens")
def create_store_tokens():
    datahandler.store_tokens(workers, aemtli, entsorgen)

@app.get("/api/health")
def health_check():
    return status.HTTP_200_OK

if __name__ == "__main__":
    uvicorn.run("main_servierer:app", host="0.0.0.0", port=8000, reload=True)