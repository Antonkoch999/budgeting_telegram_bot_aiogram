"""Аутентификация — пропускаем сообщения только от одного Telegram аккаунта"""
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from aiogram_modul.constants import AnswerEnum


class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_ids: list):
        self.access_ids = access_ids
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if int(message.from_user.id) not in self.access_ids:
            await message.answer(AnswerEnum.NO_ACCESS.value)
            raise CancelHandler()
