from enum import Enum
from pydantic import BaseModel, Field


class Channel(str, Enum):
    cellular = "cellular"
    telephone = "telephone"


class NonContextualRecommendation(BaseModel):
    recommended_channel: Channel = Field(
        ...,
        description="Canal recomendado"
    )
    policy: str = Field(
        default="thompson_sampling_non_contextual"
    )
    sampled_values: dict[str, float] = Field(
        ...,
        description="Valores amostrados da distribuição Beta para cada canal (braço/arm)"
    )
