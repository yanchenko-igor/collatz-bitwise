class Bit:
    def __init__(self, index, value, tape):
        self.index = index
        self.value = value
        self.tape = tape

    def __repr__(self):
        return f"{self.value}"


class Tape:
    def __init__(self, bit_string, debug=False):
        self.bits = {}
        for i, ch in enumerate(reversed(bit_string)):
            self.bits[i] = Bit(i, int(ch), self)
        self.postponed_carries = {}  # postponed carries beyond current bits
        self.debug = debug

    def ensure(self, index):
        if index not in self.bits:
            # Create new bit initialized with 0
            self.bits[index] = Bit(index, 0, self)
            # Apply postponed carries for this bit if any
            if index in self.postponed_carries:
                carry_val = self.postponed_carries.pop(index)
                old_val = self.bits[index].value
                total = old_val + carry_val
                self.bits[index].value = total % 2
                overflow = total // 2
                if overflow > 0:
                    # Postpone overflow carry to next bit
                    self.postponed_carries[index + 1] = self.postponed_carries.get(index + 1, 0) + overflow
                if self.debug:
                    print(f"[Postponed carry applied] Bit[{index}]: {old_val} + {carry_val} -> {self.bits[index].value} overflow {overflow}")
        return self.bits[index]

    def add_carry(self, index, carry_val):
        if carry_val == 0:
            return
        old_val = self.bits[index].value if index in self.bits else 0
        total = old_val + carry_val
        new_val = total % 2
        overflow = total // 2

        if index in self.bits:
            if new_val == old_val and overflow == 0:
                # No change, no carry — stop here
                return
            self.bits[index].value = new_val
        else:
            # Only create bit if new_val != 0 or overflow > 0
            if new_val == 0 and overflow == 0:
                return
            self.bits[index] = Bit(index, new_val, self)

        if self.debug:
            print(f"[Add carry] Bit[{index}]: {old_val} + {carry_val} -> {new_val} overflow {overflow}")

        if overflow > 0:
            self.add_carry(index + 1, overflow)


    def to_binary_string(self):
        max_index = max((i for i in self.bits if self.bits[i].value != 0), default=0)
        return ''.join(str(self.ensure(i).value) for i in reversed(range(0, max_index + 1))) or '0'

    def is_one(self):
        return (
            self.ensure(0).value == 1 and
            all(self.ensure(i).value == 0 for i in range(1, max(self.bits.keys()) + 1))
        )


class CollatzMachine:
    def __init__(self, tape):
        self.tape = tape

    def step(self):
        if self.tape.ensure(0).value % 2 == 0:
            # Divide by 2: shift right
            max_index = max(self.tape.bits.keys())
            for i in range(max_index):
                self.tape.ensure(i).value = self.tape.ensure(i + 1).value
            # Remove last bit
            self.tape.bits.pop(max_index, None)
            if self.tape.debug:
                print(f"[div2] Tape: {self.tape.to_binary_string()}")
        else:
            # Apply (3n + 1): (n << 1) + n + 1
            original = {i: self.tape.ensure(i).value for i in self.tape.bits}
            max_index = max(original.keys())

            # Shift left (n << 1)
            for i in reversed(range(max_index + 1)):
                self.tape.ensure(i + 1).value = self.tape.ensure(i).value
            self.tape.ensure(0).value = 0

            # Add original back (+ n)
            carry = 0
            for i in range(max_index + 2):
                old_val = self.tape.ensure(i).value
                add_val = original.get(i, 0)
                total = old_val + add_val + carry
                self.tape.ensure(i).value = total % 2
                carry = total // 2
            if carry > 0:
                self.tape.add_carry(max_index + 2, carry)

            # Add 1 (+1)
            self.tape.add_carry(0, 1)

            if self.tape.debug:
                print(f"[3n+1] Tape: {self.tape.to_binary_string()}")

    def run_until_done(self, max_steps=1000):
        steps = 0
        while not self.tape.is_one() and steps < max_steps:
            self.step()
            steps += 1
        return steps


if __name__ == "__main__":
    tape = Tape("11011")  # 27 in binary
    machine = CollatzMachine(tape)
    steps = machine.run_until_done()
    print("Final state:", tape.to_binary_string())
    print("Steps taken:", steps)

