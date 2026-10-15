"""Independent mathematical verification; never trust LLM arithmetic."""
import math
from dataclasses import dataclass

TRIPLES = [(3,4,5),(5,12,13),(6,8,10),(8,15,17),(7,24,25),(9,12,15),(9,40,41),(12,16,20),(15,20,25),(20,21,29),(12,35,37),(11,60,61),(16,30,34),(28,45,53),(33,56,65)]

@dataclass(frozen=True)
class Problem:
    level: str
    story: str
    a: int
    b: int
    c: int
    unknown: str
    hint: str
    explanation: str

    @property
    def answer(self) -> int:
        return {'a':self.a,'b':self.b,'c':self.c}[self.unknown]

    @property
    def signature(self) -> str:
        return f'{self.a}-{self.b}-{self.c}-{self.unknown}'


def validate(data: dict, level: str) -> Problem:
    required = ('level','story','a','b','c','unknown','hint','explanation')
    if not isinstance(data,dict) or any(k not in data for k in required):
        raise ValueError('AI output is missing required fields.')
    if data['level'] != level or data['unknown'] not in ('a','b','c'):
        raise ValueError('Invalid level or unknown side.')
    for k in ('a','b','c'):
        if type(data[k]) is not int or not 0 < data[k] <= 100:
            raise ValueError('Side lengths must be positive integers <= 100.')
    a,b,c = (data[k] for k in ('a','b','c'))
    if a*a+b*b != c*c or c <= max(a,b):
        raise ValueError('Not a valid right triangle.')
    if level == 'Foundation' and (data['unknown'] != 'c' or c > 17):
        raise ValueError('Foundation problem must have a small missing hypotenuse.')
    if level != 'Foundation' and data['unknown'] == 'c':
        raise ValueError('Standard/Advanced should ask for a leg.')
    for k in ('story','hint','explanation'):
        if not isinstance(data[k],str) or not data[k].strip() or len(data[k]) > 1200:
            raise ValueError('Missing or oversized text.')
    # We cannot formally prove that free-form story text matches the numbers;
    # therefore the app builds its displayed question deterministically.
    return Problem(**{k:data[k] for k in required})


def question(p: Problem) -> str:
    unit = 'cm'
    if p.unknown == 'c':
        return f'A right triangle has perpendicular legs of {p.a} {unit} and {p.b} {unit}. Find the hypotenuse c.'
    known_leg = p.b if p.unknown == 'a' else p.a
    return f'A right triangle has a hypotenuse of {p.c} {unit} and one leg of {known_leg} {unit}. Find the other leg ({p.unknown}).'


def steps(p: Problem) -> list[str]:
    if p.unknown == 'c':
        return ['Use a² + b² = c².',f'{p.a}² + {p.b}² = c²',f'{p.a*p.a} + {p.b*p.b} = {p.c*p.c}',f'c = √{p.c*p.c} = {p.c} cm']
    known = p.b if p.unknown == 'a' else p.a
    return ['Use a² + b² = c².',f'{p.unknown}² = {p.c}² − {known}²',f'{p.unknown}² = {p.c*p.c} − {known*known} = {p.answer*p.answer}',f'{p.unknown} = √{p.answer*p.answer} = {p.answer} cm']


def is_correct(answer: str, p: Problem) -> bool:
    try:
        value=float(answer.strip().replace(',','.'))
        return math.isfinite(value) and math.isclose(value,p.answer,abs_tol=0.01,rel_tol=0)
    except (ValueError,AttributeError):
        return False
