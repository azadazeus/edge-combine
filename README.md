# Edge Combiner

Combine multiple `.edge` adjacency‑matrix files (square, whitespace‑delimited) into a single block‑diagonal super‑matrix—largest component first—using a simple cross‑platform CLI.

---

## Features

| Feature                     | Description                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------ |
| **Largest‑first ordering**  | Automatically sorts input files so the biggest matrix occupies the upper‑left block.             |
| **Block‑diagonal merge**    | Produces a sparse‑friendly representation: original matrices remain intact, surrounded by zeros. |
| **One‑line CLI**            | `python combine_edges.py <folder> [options]`—that’s it.                                          |
| **Zero heavy dependencies** | Only needs *NumPy* and *SciPy*.                                                                  |
| **Wide OS support**         | Tested on Windows 10/11, macOS 12+, Ubuntu 22.04.                                                |

---

## Requirements

* Python ≥ 3.8
* `numpy`
* `scipy`

Install the scientific stack any way you like:

```bash
pip install numpy scipy
```

---

## Installation

```bash
git clone https://github.com/<your‑username>/edge‑combiner.git
cd edge‑combiner
```

(Optional) create a virtual environment first.

---

## Quick Start

### CLI

```bash
python combine_edges.py <folder>               # default output total.edge
python combine_edges.py <folder> -o big.edge   # custom name
python combine_edges.py <folder> -p 8          # keep 8 decimal places
```

* `<folder>` – directory containing individual `.edge` files.
* `-o/--output` – filename for the combined matrix (default `total.edge`).
* `-p/--precision` – decimals retained when writing floats (default 5).
* `-a/--alphabetically` - sort alphabetically
* `-s/--size` - sort by size (largest first)

#### Windows (PowerShell)

```powershell
python combine_edges.py "C:\Users\edge data" -p 8
```

#### macOS / Linux

```bash
./combine_edges.py ~/edge_data -o mega.edge
```

### Programmatic use

```python
from combine_edges import combine_edge_folder
combine_edge_folder(r"C:\Users\edge data", output_name="mega.edge", precision=6)
```

---

## What it Does

1. **Discovers** every `.edge` file in the target folder (ignoring any existing `total.edge`).
2. **Validates** each file is square; throws a descriptive error if not.
3. **Stitches** them into a block‑diagonal mega‑matrix with `scipy.linalg.block_diag`.
4. **Writes** the result back into the same folder.

The final layout looks like this:

```
┌──── A (big) ────┐ 0           0
│                 │             │
│                 │             │
├────────────┬────┼──── B ──────┤ 0
│            │    │             │
│     0      │    │             │
└────────────┴────┴─────────────┘ C (small)
```

---

## Contributing

Pull requests are welcome!  Open an issue first if you’d like to discuss a change.

```bash
git checkout -b feature/your‑idea
# … hack hack hack …
git commit -m "Add amazing feature"
git push origin feature/your‑idea
```

---

## License

This project is released under the MIT License—see [LICENSE](LICENSE) for details.

---

## Troubleshooting

| Symptom                          | Possible cause                                      | Fix                                                                                          |
| -------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `ValueError: not square`         | File has blank lines or unequal row / column counts | Open the file, remove extra whitespace, or regenerate it correctly.                          |
| `ModuleNotFoundError: scipy`     | SciPy not installed                                 | `pip install scipy`                                                                          |
| Output zeros where data expected | Files mis‑ordered?                                  | Verify filenames & folder path; script ignores `total.edge` but everything else is included. |

---

## Platform Notes

* **Windows:** Runs in PowerShell, Command Prompt, or Git Bash. Shebang line is ignored; call with `python`.
* **macOS/Linux:** Make the script executable (`chmod +x combine_edges.py`) to run as `./combine_edges.py`.
* **WSL:** Treat as Linux—just ensure Python is installed inside WSL.
