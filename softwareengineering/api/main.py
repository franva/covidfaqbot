from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from answor import Answor

app = FastAPI()
classifier = Answor()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return 200


@app.get('/t/{text}')
async def translate(text: str):
    if text:
        result = classifier.get_prediction(text)
        # resultJson = {
        #     "category": result[],
        #     "probability": result[1]
        # }
        json_compatible_item_data = jsonable_encoder(result)
        return JSONResponse(content=json_compatible_item_data)


    return {'invalid text'}
