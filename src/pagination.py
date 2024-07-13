# global module e.g. pagination
from typing import Optional
from fastapi import Query

class PaginationParams:
    def __init__(self, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
        self.skip = skip
        self.limit = limit
