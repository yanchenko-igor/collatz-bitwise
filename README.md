# Collatz Bitwise Machine

This project presents a **bitwise, streaming implementation of the Collatz Conjecture**. Rather than operating on full integers, it models each Collatz step as a finite-state machine that consumes input one bit at a time (LSB-first) and produces transformed output in real-time.

This proves that the Collatz transformation:

- ✅ Is computable without access to the full input
- ✅ Works incrementally and recursively
- ✅ Preserves correctness for arbitrarily long integers
- ✅ Can be chained to produce the full Collatz sequence

---

## 📁 Project Structure

```
.
├── LICENSE               # CC0 Public Domain Dedication
├── README.md             # This file
├── collatz_machine.py    # The CollatzMachine class (bitwise logic)
├── demo.py               # Demo: runs Collatz on 27 recursively
└── main.tex              # LaTeX paper for arXiv submission
```

---

## 🧠 What Is This?

The **Collatz Conjecture** posits that for any integer `n > 0`, repeated application of:

- If even: `n → n / 2`
- If odd: `n → 3n + 1`

...eventually reaches `1`.

This project implements each step as a **bitwise transformation**, driven by machines that:

- Take bits LSB-first
- Stream the output
- Require no knowledge of the full number

---

## 🚀 Quick Start

### 🐍 Run the Demo

```bash
python3 demo.py
```

You’ll see the full Collatz trajectory for `27` printed to the terminal.

### 📦 Example Output

```
--- Collatz Chain for 27 ---
Step 0: 27 → 82
Step 1: 82 → 41
Step 2: 41 → 124
...
Step 110: 2 → 1
Step 111: 1 → 1
```

---

## 🧪 Core Logic

See [`collatz_machine.py`](./collatz_machine.py) for the `CollatzMachine` class, which exposes:

```python
m = CollatzMachine()
m.nextbit(1)
m.nextbit(0)
...
m.end_of_input()
print(m.report())
```

Each machine represents **one transformation** (`n → n/2` or `3n+1`), and its output can be fed into the next machine in a chain.

---

## 📄 Research Paper

The mathematical write-up and proof sketch are in [`main.tex`](./main.tex), suitable for submission to arXiv. It includes:

- Bitwise formulation of Collatz
- Construction of the machine
- Theorem and sketch proof
- Implications for computation theory

To compile:

```bash
pdflatex main.tex
```

---

## 📜 License

This work is released into the **public domain** under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) dedication.

> You may copy, modify, distribute, and use the work, even for commercial purposes, all without asking permission.

See [`LICENSE`](./LICENSE).

---

## 🙌 Contributing

Forks and experiments welcome. No attribution required. If you improve the structure, visualization, or apply it in symbolic computation or formal verification, feel free to open an issue or share your fork.

---

