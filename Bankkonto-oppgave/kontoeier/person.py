from dataclasses import dataclass, field


@dataclass
class Person:
    navn: str
    etternavn: str
    telefonnummer: str
    alder: int
    bankkontoer: list = field(default_factory=lambda: [])
