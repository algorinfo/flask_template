import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class S3:
    key: Optional[str] = os.getenv("CHANGEME_SPACES_KEY")
    secret: Optional[str] = os.getenv("CHANGEME_SPACES_SECRET")
    endpoint: Optional[str] = os.getenv("CHANGEME_SPACES_ENDPOINT")


@dataclass
class Config:
    """ General config """
    SQL: Optional[str] = os.getenv("CHANGEME_SQL")
    SECRET_KEY: Optional[bytes] = os.getenv("SECRET_KEY").encode("utf-8")
    REDIS: Optional[str] = os.getenv("CHANGEME_REDIS")
    QNAME: Optional[str] = os.getenv("CHANGEME_QNAME")

    # S3 configuration
    spaces: Optional[S3] = None


