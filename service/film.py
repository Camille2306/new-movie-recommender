from dataclasses import dataclass
from typing import Optional, List


@dataclass
class MovieProfile:

    #id: int
    title: str

    runtime: Optional[int]

    release_year: Optional[int]

    language: Optional[str]

    #popularity: Optional[float]

    #vote_average: Optional[float]

    #vote_count: Optional[int]

    genres: Optional[List[str]] = None

    black_and_white: Optional[bool] = None

    silent: Optional[bool] = None

    sadness: Optional[float] = None