# Guitar Chord Reference

A comprehensive visual guide to guitar chords, typeset in LaTeX using TikZ.

## Overview

This project provides a high-quality, printable PDF reference for guitar chords in standard tuning (**E A D G B e**). It includes visual diagrams for a wide variety of chord shapes, designed for clarity and ease of use.

## Files

- `guitar_chords.tex`: The LaTeX source code.
- `guitar_chords.pdf`: The compiled, ready-to-print reference guide.
- `LICENSE`: MIT License.

## Building from Source

To compile the PDF from the LaTeX source, you will need a LaTeX distribution (such as TeX Live or MiKTeX) installed on your system.

Use `pdflatex` to generate the PDF:

```bash
pdflatex guitar_chords.tex
```

Note: You may need to run it twice to ensure all references and formatting are correctly processed.

### Dependencies

The following LaTeX packages are used:
- `tikz` (for chord diagrams)
- `geometry`
- `xcolor`
- `titlesec`
- `fancyhdr`
- `booktabs`
- `longtable`

## License

This project is licensed under the [MIT License](LICENSE).

---
Copyright (c) 2026 Fabian Bastin
