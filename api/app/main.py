from pathlib import Path
from collections import namedtuple
import json
import numpy as np
from fastapi import FastAPI

from app.schemas.request_schemas import CustomerRequest
from app.schemas.response_schemas import NonContextualRecommendation


app = FastAPI()
rng = np.random.default_rng()

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"
with open(ARTIFACTS_DIR / "non_contextual_bandit.json") as f:
    arm_params_raw = json.load(f)

ArmParams = namedtuple("ArmParams", ["alpha", "beta"])
arm_params = {arm: ArmParams(**params) for arm, params in arm_params_raw.items()}


@app.post(
    "/recommend/non-contextual",
    response_model=NonContextualRecommendation,
    description="Recomenda um canal de contato utilizando Thompson Sampling não contextual"
)
def recommend_non_contextual(customer: CustomerRequest) -> NonContextualRecommendation:
    arm_probs = {arm: rng.beta(params.alpha, params.beta) for arm, params in arm_params.items()}
    chosen_arm = max(arm_probs, key=arm_probs.get)

    return NonContextualRecommendation(
        recommended_channel=chosen_arm,
        sampled_values=arm_probs,
    )
