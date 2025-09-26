from fastapi import APIRouter


router = APIRouter()


@router.get("/", response_model=str)
def home_page():
    return "Welcome to Gitsy!"


@router.get("/get-started", response_model=str)
def get_started():
    return "Let's get started with Gitsy!"


@router.get("/create-report", response_model=str)
def create_report_page():
    return "Let's create a report!"
