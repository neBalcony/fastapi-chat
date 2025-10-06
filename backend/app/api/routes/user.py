from fastapi import APIRouter, HTTPException
from app.api.deps import CurrentUser, SessionDep
from app.models.models import User
from app.schemas.user import UserRegister,UserRead

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserRead)
def get_user(session: SessionDep, current_user: CurrentUser):
    return UserRead.model_validate(current_user)

# TODO create one superuser and add another account use him + init superuser if dosent exist from .env
@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(user_id: int, session: SessionDep):
	user = session.get(User, user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")

	return UserRead.model_validate(user)

# TODO: Delete when authorization is implemented
@router.post("/", response_model=UserRead)
def update_user(user_in: UserRegister, session: SessionDep):
	user = User(
		username = user_in.username,
		#TODO:Make hashed
		hashed_password = user_in.password
	)
	session.add(user)
	session.commit()
	session.refresh(user)
	return UserRead.model_validate(user)

