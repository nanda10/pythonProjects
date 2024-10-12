"""decorator used to Handle session"""
import functools

from typing import Callable
from pymongo.errors import PyMongoError
from fastapi.exceptions import HTTPException


def transactional(func: Callable) -> Callable:
    """open transaction according to available session"""

    @functools.wraps(func)
    async def _wrapper(*args, **kwargs):
        try:
            with kwargs["request"].app.client.start_session() as session:
                with session.start_transaction():
                    try:
                        result = await func(*args, **kwargs, _session=session)
                        session.commit_transaction()
                        return result
                    except PyMongoError as exc:
                        session.abort_transaction()
                        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(exc)}")
        except PyMongoError as exc:
            raise HTTPException(status_code=500, detail=f"Some issue while connecting to db. Try again")

            
    return _wrapper