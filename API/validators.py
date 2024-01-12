from pydantic import BaseModel, field_validator


class QuestionnaireAnswers(BaseModel):
    budget: str
    male: str
    age: str
    date_type: str
    hobbies: str
    related_gifts: str
    favorite_color: str

    @field_validator("budget", "male", "age")
    @classmethod
    def must_contain_integer_and_must_be_greater_than_zero(cls, value: str) -> str:
        if not isinstance(int(value), int):
            raise ValueError("Must contain an integer")
        if int(value) <= 0:
            raise ValueError("Must be greater than zero")
        return value

    @field_validator("male")
    @classmethod
    def must_be_one_or_two(cls, value: str) -> str:
        if value == "1" or value == "2":
            return value
        raise ValueError("Must be one or two")


class RecommendedProduct(BaseModel):
    name: str
    price: str
    image_url: str
    link: str
