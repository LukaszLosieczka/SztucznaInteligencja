class Layout:

    def __init__(self, machines: [(int, int)], full_cost=0):
        self.machines = machines
        self.full_cost = full_cost

    def get_machine_coordinates(self, number):
        return self.machines[number]

    def number_of_machines(self):
        return len(self.machines)

    def __getitem__(self, key):
        return self.machines[key]

    def __str__(self):
        return f"{self.machines}, cost: {self.full_cost}"
