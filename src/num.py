class NUM:
    def __init__(self, n = 0, s = ""):
        self.at = n
        self.txt = s
        self.n = 0
        self.lo = float('inf')
        self.hi = float('-inf') # Replaced sys.maxsize
        self.ok = True
        self.has = {}
        self.w = -1 if s.endswith("-") else 1