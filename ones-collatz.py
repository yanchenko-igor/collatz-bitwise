class OnePositionsCollatz:
    def __init__(self, n, debug=False):
        self.debug = debug
        self.step_count = 0
        self.positions = self.int_to_positions(n)

    @staticmethod
    def int_to_positions(val):
        positions = set()
        pos = 0
        while val > 0:
            if val & 1:
                positions.add(pos)
            val >>= 1
            pos += 1
        return positions

    @staticmethod
    def positions_to_int(positions):
        val = 0
        for p in positions:
            val |= (1 << p)
        return val

    def step(self):
        self.step_count += 1
        n = self.positions_to_int(self.positions)
        if self.debug:
            bit_str = self.reconstruct_bitstring()
            print(f"Step {self.step_count}: n={n} bits={bit_str}")

        if n == 1:
            return False  # collapsed to 1, stop

        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

        self.positions = self.int_to_positions(n)
        return True

    def run(self):
        while self.step():
            pass
        if self.debug:
            print(f"Collapsed to 1 in {self.step_count} steps.")

    def reconstruct_bitstring(self):
        if not self.positions:
            return '0'
        highest = max(self.positions)
        bits = ['0'] * (highest + 1)
        for p in self.positions:
            bits[-1 - p] = '1'  # MSB on left
        return ''.join(bits)


if __name__ == "__main__":
    machine = OnePositionsCollatz(27, debug=True)
    machine.run()

