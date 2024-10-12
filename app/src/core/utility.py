from ast import List
from datetime import datetime
import uuid
from fastapi.responses import JSONResponse
from sqids import Sqids
import numpy as np


class Utility:
    squids = Sqids(
        alphabet="Kj3eblC5ocwv682gTtdMQIZpWH7hJsLkS0BP4EGruUYyqAOXm9nfxizVaRDFN1",
        min_length=16
    )

    @staticmethod
    def json_response(status, message, error, data):
        return JSONResponse({
            "status": status,
            "message": message,
            "error": error,
            "data": data
        })

    @staticmethod
    def dict_response(status, message, error, data):
        return ({
            "status": status,
            "message": message,
            "error": error,
            "data": data
        })

    @staticmethod
    def uuid():
        return str(uuid.uuid4())

    @staticmethod
    def pagination(status: int, message: str, error: List, data: List | None, total: int, limit: int, offset: int):
        return ({
            "status": status,
            "message": message,
            "errors": error,
            "data": ({
                "content": data if data else [],
                "total": total,
                "limit": limit,
                "offset": offset
            })
        })

    @staticmethod
    def encodeId(id: int):
        now = datetime.now()
        list_int = [
            *map(int, f"{now.second:02}{now.minute:02}{now.day:02}{now.month:02}"),
            id, *map(int, f"{now.year:04}")
        ]
        return Utility.squids.encode(list_int)

    @staticmethod
    def decodeId(id: str):
        try:
            return Utility.squids.decode(id)[-5]
        except ValueError:
            return 0

# print(Utility.uuid())
