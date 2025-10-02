from fastapi import Request
from fastapi.responses import JSONResponse


class ResourceNotFoundException(Exception):
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id


async def resource_not_found_exception_handler(request: Request, exc: ResourceNotFoundException):
    return JSONResponse(status_code=404, content={"message": f"{exc.name} with id {exc.id} not found"})


