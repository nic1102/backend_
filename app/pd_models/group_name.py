from pydantic import BaseModel, field_validator


class GroupName(BaseModel):
    group_name: str


    @field_validator('group_name')
    @classmethod
    def validate_group_name(cls, value: str) -> str:
        bad_symbols = ['{', '}', '/', '\\', '=', '+', '*', '@', '%', '&', '~']
        for i in bad_symbols:
            if i in value:
                raise ValueError(f'Недопустимый символ - {i}')
        return value