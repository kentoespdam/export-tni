import uuid
from ast import List
from datetime import datetime

from fastapi.responses import JSONResponse
from sqids import Sqids

from .config import settings

class Utility:
    squids = Sqids(
        alphabet=settings.SQUIDS_ALPHABET,
        min_length=settings.SQUIDS_MIN_LENGTH,
    )

    @staticmethod
    def json_response(status, message, error, data):
        return JSONResponse(
            {"status": status, "message": message, "error": error, "data": data}
        )

    @staticmethod
    def dict_response(status, message, error, data):
        return {"status": status, "message": message, "error": error, "data": data}

    @staticmethod
    def uuid():
        return str(uuid.uuid4())

    @staticmethod
    def pagination(
        status: int,
        message: str,
        error: List,
        data: List | None,
        total: int,
        limit: int,
        page: int,
        totalPages: int,
        isFirst: bool,
        isLast: bool,
    ):
        return {
            "status": status,
            "message": message,
            "errors": error,
            "data": (
                {
                    "content": data if data else [],
                    "total": total,
                    "limit": limit,
                    "page": page,
                    "totalPages": totalPages,
                    "isFirst": isFirst,
                    "isLast": isLast,
                }
            ),
        }

    @staticmethod
    def encodeId(id: int):
        now = datetime.now()
        list_int = [
            *map(int, f"{now.second:02}{now.minute:02}{now.day:02}{now.month:02}"),
            id,
            *map(int, f"{now.year:04}"),
        ]
        return Utility.squids.encode(list_int)

    @staticmethod
    def decodeId(id: str):
        try:
            return Utility.squids.decode(id)[-5]
        except ValueError:
            return 0
