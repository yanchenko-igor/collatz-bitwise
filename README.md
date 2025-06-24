# CollatzMachine — Bitwise Collatz Sequence Simulator

## Overview

`CollatzMachine` simulates the Collatz sequence on a binary tape using pure bitwise operations. It models the process as an in-place Turing-like machine, manipulating bits without cloning or unnecessary overhead.

- Operates on a **binary tape** represented as a list of bits (LSB at index 0).
- Implements **exact binary shift and add operations** to perform the Collatz step:
  - Even numbers → divide by 2 (right shift).
  - Odd numbers → `3n + 1` (bit-shift left, add original, add 1).
- Uses **postponed carries only for bits beyond current tape length**, ensuring minimal bit creation.
- Fully **in-place**, no tape cloning or state duplication.
- Designed for **precise control** over bit mutation and carry propagation.
- Provides optional **debug mode** for step-by-step internal state tracing.

## Features

- Handles arbitrary binary inputs as strings (e.g. `"101"`, `"11011"`).
- Automatically grows tape as needed only when result requires new bits.
- Stops execution once tape reaches the value 1 (`0b1`).
- Supports inspecting current tape state as a binary string.
- Minimal and efficient — no unnecessary object creation or memory waste.

## Usage

```python
from collatz_machine import Tape, CollatzMachine

# Initialize tape with binary string (LSB at right)
tape = Tape("101", debug=True)  # binary 5

machine = CollatzMachine(tape)

steps = machine.run_until_done()

print("Final binary:", tape.to_binary_string())  # Output: 1
print("Steps taken:", steps)                      # Number of Collatz steps
```

## API

### Tape

- `Tape(bit_string: str, debug=False)`: Create tape from binary string.
- `ensure(index)`: Get bit at index, creating if missing and applying postponed carries.
- `add_carry(index, carry_val)`: Add carry to bit, postponing if bit not yet created.
- `to_binary_string()`: Get current binary tape string (MSB to LSB).
- `is_one()`: Check if tape represents the number 1.

### CollatzMachine

- `CollatzMachine(tape)`: Initialize with a Tape.
- `step()`: Perform one Collatz step.
- `run_until_done(max_steps=1000)`: Run steps until tape equals 1 or max steps reached.

## Design Notes

- Postponed carries only stored for **non-existing bits**; applied immediately on creation.
- Bit indexing starts at 0 (least significant bit).
- Debug logs provide trace of carry propagation and bit mutation.
- Avoids unnecessary bit creation by halting carry propagation when no effect.

## Philosophy

This tool embodies the principle of **maximal autonomy and minimal interference**:

- No hidden state cloning or overhead.
- Total transparency and control over bit-level operations.
- Efficient, market-driven logic of binary computation without coercion.

## License

Public Domain — free and unbound.
