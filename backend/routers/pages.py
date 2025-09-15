from fastapi import APIRouter


router = APIRouter()


@router.get("/", response_model=str)
def home_page():
    return "Welcome to Gitsy!"


@router.get("/get-started", response_model=str)
def get_started():
    return "Let's get started with Gitsy!"
