from pydantic import BaseModel, Field, model_validator


class GeneralSchema(BaseModel):
    hello: str = Field(..., max_length=128)
    key1: int = Field(..., ge=0)

    @model_validator(mode="after")
    def check_key1(self):
        if self.key1 == 10:
            raise ValueError("Не должно быть 10")
        return self
