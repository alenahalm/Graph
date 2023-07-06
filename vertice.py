
class Vertice():
    
    def __init__(self, id, edges, is_sp, pair) -> None:
        self.id = id
        self.edges = edges
        self.is_sp = is_sp
        self.pair = pair
    
    def clear(self):
        self.id = 0
        self.edges = []
        self.is_sp = False
        self.pair = 0

    def __str__(self) -> str:
        return f'{self.id}, {self.edges}, is_showplace: {self.is_sp}, pair: {self.pair}'

    def copy(self):
        return Vertice(self.id, self.edges.copy(), self.is_sp, self.pair)