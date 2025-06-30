#!/usr/bin/env python
"""
Combine multiple .edge adjacency-matrix files into a single
block-diagonal mega-matrix called total.edge (or a name you choose).

Usage
-----
python combine_edges.py  <folder>                    # default: directory order, total.edge
python combine_edges.py  <folder>  -o   my_result.edge
python combine_edges.py  <folder>  -p   8            # 8-decimal precision
python combine_edges.py  <folder>  -a                # sort alphabetically
python combine_edges.py  <folder>  -s                # sort by size (largest first)
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
                        precision: int = 5,
                        sort_mode: str = "directory") -> Path:
    """Assemble .edge files into one block-diagonal file with specified sorting."""
    edge_files = [p for p in folder.glob("*.edge") if p.name != output_name]
    if not edge_files:
        raise FileNotFoundError("No .edge files found in the folder.")
    
    # Sort files based on the specified mode
    if sort_mode == "alphabetical":
        edge_files.sort()  # alphabetical order
        sort_description = "alphabetical order"
    elif sort_mode == "size":
        edge_files.sort(key=edge_size, reverse=True)  # largest matrix first
        sort_description = "size (largest first)"
    else:  # directory order (default)
        # Keep the order as found by glob, which is typically directory order
        # but ensure consistency across systems by sorting without any key
        edge_files = sorted(edge_files, key=lambda x: x.name)
        sort_description = "directory order"
    
    blocks = [read_edge(p) for p in edge_files]
    combined = block_diag(*blocks)
    
    out_path = folder / output_name
    np.savetxt(out_path,
               combined,
               fmt=f"%.{precision}f",
               delimiter=" ")
    
    print(f"\n✔ Combined order ({sort_description}):")
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
    
    # Sorting options - mutually exclusive
    sort_group = parser.add_mutually_exclusive_group()
    sort_group.add_argument("-a", "--alphabetical",
                           action="store_true",
                           help="Sort files alphabetically")
    sort_group.add_argument("-s", "--size",
                           action="store_true",
                           help="Sort files by size (largest first)")
    
    args = parser.parse_args()
    
    # Determine sorting mode
    if args.alphabetical:
        sort_mode = "alphabetical"
    elif args.size:
        sort_mode = "size"
    else:
        sort_mode = "directory"  # default
    
    combine_edge_folder(args.folder.resolve(),
                        output_name=args.output,
                        precision=args.precision,
                        sort_mode=sort_mode)


if __name__ == "__main__":
    main()
