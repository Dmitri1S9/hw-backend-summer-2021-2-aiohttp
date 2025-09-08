from dataclasses import dataclass
from typing import List


@dataclass
class Theme:
    id: int | None
    title: str

@dataclass
class Answer:
    title: str
    is_correct: bool

@dataclass
class Question:
    id: int
    theme_id: int
    title: str
    answers: List[Answer] | None




