from pydantic import BaseModel, field_validator


class SongName(BaseModel):
    song_name: str

    @field_validator('song_name')
    @classmethod
    def validate_song_name(cls, value: str) -> str:
        bad_symbols = ['{', '}', '/', '\\', '=', '+', '*', '@', '%', '&', '~']
        for i in bad_symbols:
            if i in value:
                raise ValueError(f'Недопустимый символ - {i}')
        return value