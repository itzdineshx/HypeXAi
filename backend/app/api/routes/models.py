from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.db.session import get_db
from app.schemas.playground import PlaygroundSimulationRequest, PlaygroundSimulationResponse
from app.services.meme_dataset_scoring import score_meme_coin_dataset
from app.services.model_training import train_all_models
from app.services.playground_simulation import simulate_playground

router = APIRouter()


@router.post("/train-all")
def train_models(db: Database = Depends(get_db)) -> dict[str, dict]:
    return train_all_models(db)


@router.post("/score-meme-data")
def score_meme_data(db: Database = Depends(get_db)) -> dict[str, object]:
    return score_meme_coin_dataset(db=db)


@router.post("/playground-simulate", response_model=PlaygroundSimulationResponse)
def playground_simulate(payload: PlaygroundSimulationRequest, _: Database = Depends(get_db)) -> PlaygroundSimulationResponse:
    return simulate_playground(payload)