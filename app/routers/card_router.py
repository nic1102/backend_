from fastapi import APIRouter

card_router = APIRouter(prefix="/card")

@card_router.get("/")
def get_card():
    #group name
    #song name
    #likes
    #dislikes
    #quote text
    ...
