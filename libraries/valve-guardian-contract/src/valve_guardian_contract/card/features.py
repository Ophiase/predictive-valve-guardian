from typing import Annotated

from pydantic import BaseModel, Field


class FeatureSettings(BaseModel):
    order: Annotated[int, Field(ge=0, le=2)] = Field(
        default=0, description="Statistics up to this finite difference."
    )
    fourier_coefficients: Annotated[int, Field(ge=0)] = Field(
        default=0, description="FFT magnitudes kept per signal; 0 for none."
    )
