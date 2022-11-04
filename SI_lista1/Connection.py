class Connection:

    def __init__(self, source: int, destination: int, cost: int, amount: int):
        self.source = source
        self.destination = destination
        self.cost = cost
        self.amount = amount

    def __hash__(self):
        return hash((self.source, self.destination))

    def __eq__(self, other):
        return (self.source, self.destination) == (other.source, other.destination)

    def __str__(self):
        return f"source: {self.source}, dest: {self.destination}, cost: {self.cost}, amount: {self.amount}"
