from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import datetime
import dblogic
import uvicorn

dblogic.create_tables()
dblogic.create_highscore()
app = FastAPI()

class CheckinRequest(BaseModel):
    token: str = Field(..., description="User's unique token")
    timestamp: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

class CheckinResponse(BaseModel):
    success: bool
    message: str

class HighscoreResponse(BaseModel):
    worker_name: str
    work_done: int

@app.post("/api/save_checkin", response_model=CheckinResponse)
def api_save_checkin(
    request: CheckinRequest,
):
    if request.token not in dblogic.tokens:
        raise HTTPException(status_code=418, detail="Invalid token")

    success = dblogic.save_checkin(request.token, request.timestamp)
    if success:
        return CheckinResponse(success=True, message="Check-in saved successfully")
    else:
        raise HTTPException(status_code=500, detail="Failed to save check-in")

@app.get("/api/check_work")
def api_check_work():
    if dblogic.update_work_done():
        return status.HTTP_200_OK
    else:
        return status.HTTP_503_SERVICE_UNAVAILABLE

@app.get("/api/highscores", response_model=List[HighscoreResponse])
def get_highscores():
    highscore_query = dblogic.get_highscore()
    success = highscore_query[0]
    highscores = highscore_query[1]
    if success:
        return [HighscoreResponse(worker_name=hs.worker_name, work_done=hs.work_done) for hs in highscores]
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch Highscores")

@app.get("/api/health")
def health_check():
    return status.HTTP_200_OK

# Additional endpoints can be added as needed

if __name__ == "__main__":
    uvicorn.run("main_db:app", host="0.0.0.0", port=8001, reload=True)
