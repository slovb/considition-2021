from dataclasses import dataclass

@dataclass
class Package:
    id: int
    length: int
    width: int
    height: int
    weightClass: int
    orderClass: int

    def area(self) -> int:
        return self.width * self.length
    
    def is_heavy(self) -> bool:
        return self.weightClass == 2
