from fastapi import APIRouter
from chatbot.routers.user import router as user
from chatbot.routers.login import router as login
from chatbot.routers.chat_prompt import router as chat_prompt
from chatbot.routers.history import router as history
from chatbot.routers.stats import router as stats

router=APIRouter()

router.include_router(user)
router.include_router(login)
router.include_router(chat_prompt)
router.include_router(history)
router.include_router(stats)

