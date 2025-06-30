#!/usr/bin/env python
"""
Combine multiple .edge adjacency-matrix files into a single
block-diagonal mega-matrix called total.edge (or a name you choose).
Usage
-----
python combine_edges.py  <folder>       # default name total.edge
python combine_edges.py  <folder>  -o   my_result.edge
python combine_edges.py  <folder>  -p   8              # 8-decimal precision
"""
from pathlib import Path
import argparse
import numpy as np
from scipy.linalg import block_diag

# ---------- helper functions ----------------------------------------------- #

def edge_size(path: Path) -> int:
    """Return the matrix dimension by counting non-blank lines."""
    with path.open() as f:
        return sum(1 for line in f if line.strip())

def read_edge(path: Path) -> np.ndarray:
    """Load a square whitespace-delimited .edge file into a NumPy array."""
    rows = [
        [float(tok) for tok in ln.strip().split()]
        for ln in path.read_text().splitlines()
        if ln.strip()
    ]
    arr = np.asarray(rows, float)
    if arr.shape[0] != arr.shape[1]:
        raise ValueError(f"{path} is not square")
    return arr

def combine_edge_folder(folder: Path,
                        output_name: str = "total.edge",
                        precision: int = 5) -> Path:
    """Assemble .edge files in directory order into one block-diagonal file."""
    edge_files = [p for p in folder.glob("*.edge") if p.name != output_name]
    if not edge_files:
        raise FileNotFoundError("No .edge files found in the folder.")
    
    # Directory order (no sorting) - files processed in the order they appear in directory
    # Note: glob() returns files in directory order, which may vary by filesystem
    # but is consistent within a single run
    print(f"\n📁 Processing files in directory order:")
    for i, p in enumerate(edge_files, 1):
        print(f"   {i}. {p.name}")
    
    blocks = [read_edge(p) for p in edge_files]
    combined = block_diag(*blocks)
    
    out_path = folder / output_name
    np.savetxt(out_path,
               combined,
               fmt=f"%.{precision}f",
               delimiter=" ")
    
    print("\n✔ Combined order:")
    for p, b in zip(edge_files, blocks):
        print(f"   {p.name:>15}   ({b.shape[0]} × {b.shape[0]})")
    print(f"\n⭑ Saved {combined.shape[0]}×{combined.shape[1]} matrix → {out_path}")
    
    return out_path

# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(
        description="Combine .edge files into a block-diagonal total.edge")
    parser.add_argument("folder",
                        type=Path,
                        help="Folder containing *.edge files")
    parser.add_argument("-o", "--output",
                        default="total.edge",
                        help="Output filename (default: total.edge)")
    parser.add_argument("-p", "--precision",
                        type=int,
                        default=5,
                        help="Decimal places to keep (default: 5)")
    
    args = parser.parse_args()
    
    combine_edge_folder(args.folder.resolve(),
                        output_name=args.output,
                        precision=args.precision)

if __name__ == "__main__":
    main()
