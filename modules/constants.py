def get_ctype_elems(ctype):
    return [
        v for k, v in ctype.__dict__.items()
        if '__' not in k and 'object at' not in k
    ]

class ItemCategory:
    Clothing = "Clothing"
    ComputerComponents = "Computer Components"
    Monitors = "Monitors"
    Snacks = "Snacks"
    Other = "Other"