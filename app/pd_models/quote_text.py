from pydantic import BaseModel, field_validator


class QuoteText(BaseModel):
    quote_text: str

    @field_validator('quote_text')
    @classmethod
    def validate_song_name(cls, value: str) -> str:
        bad_symbols = ['{', '}', '/', '\\', '=', '+', '*', '@', '%', '&', '~', '[', ']']
        if len(value) > 254:
            raise ValueError(f'Превышена длина строки на {255 - len(value)} символов')
        for i in bad_symbols:
            if i in value:
                raise ValueError(f'Недопустимый символ - {i}')
        return value