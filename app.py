from fastapi import FastAPI, Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from forestCover.pipeline.training_pipeline import TrainingPipeline
from forestCover.pipeline.prediction_pipeline import PredictionPipeline
app = FastAPI()
TEMPLATES = Jinja2Templates (directory= 'templates')

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"]
)

@app.get("/", status_code=200)
@app.post("/")
async def index(request: Request):
    return TEMPLATES.TemplateResponse(name= 'index.html',
                                      context={"request": request})


@app.get("/train")
async def trainRouteClient():
    train_pipeline = TrainingPipeline()
    train_pipeline.run_pipeline()
    return Response("<h1›Training successful!!<h1>")

@app.get("/predict")
async def predictRouteClient():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
