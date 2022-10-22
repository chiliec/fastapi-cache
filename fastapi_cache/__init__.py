from typing import Callable, Optional, Type

from fastapi_cache.backends import Backend
from fastapi_cache.coder import Coder, JsonCoder
from fastapi_cache.key_builder import default_key_builder


class FastAPICache:
    _backend: Optional[Backend] = None
    _prefix: Optional[str] = None
    _expire: Optional[int] = None
    _init = False
    _coder: Optional[Type[Coder]] = None
    _key_builder: Optional[Callable] = None
    _enable = True

    @classmethod
    def init(
        cls,
        backend: Backend,
        prefix: str = "",
        expire: Optional[int] = None,
        coder: Type[Coder] = JsonCoder,
        key_builder: Callable = default_key_builder,
        enable: bool = True,
    ) -> None:
        if cls._init:
            return
        cls._init = True
        cls._backend = backend
        cls._prefix = prefix
        cls._expire = expire
        cls._coder = coder
        cls._key_builder = key_builder
        cls._enable = enable

    @classmethod
    def get_backend(cls) -> Backend:
        assert cls._backend, "You must call init first!"  # nosec: B101
        return cls._backend

    @classmethod
    def get_prefix(cls) -> Optional[str]:
        return cls._prefix

    @classmethod
    def get_expire(cls) -> Optional[int]:
        return cls._expire

    @classmethod
    def get_coder(cls) -> Optional[Type[Coder]]:
        return cls._coder

    @classmethod
    def get_key_builder(cls) -> Optional[Callable]:
        return cls._key_builder

    @classmethod
    def get_enable(cls) -> bool:
        return cls._enable

    @classmethod
    async def clear(cls, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        namespace = cls._prefix + (":" + namespace if namespace else "")
        return await cls._backend.clear(namespace, key)
