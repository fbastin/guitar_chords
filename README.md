# Guitar Chord Reference

A comprehensive visual guide to guitar chords, typeset in LaTeX using TikZ for
the diagrams and LilyPond for the staff notation.

## Overview

A printable PDF reference for guitar chords in standard tuning (**E A D G B e**).
It opens with a chord-theory chapter covering the seven natural roots A through G
— every chord type for each, with its formula and its notation — and continues
with practical fretboard voicings grouped by chord family.

## Files

| Path | Contents |
| --- | --- |
| `guitar_chords.tex` | Main document: diagrams, fingerings, summary tables. |
| `theory_chapter.tex` | The seven chord families. **Generated** — see below. |
| `gravures/` | Staff notation, one file per chord. **Generated.** |
| `outils/` | The generator and its pitch model. |
| `guitar_chords.pdf` | The compiled reference. |

## Building

Everything the document needs is committed, so LaTeX alone suffices:

```bash
pdflatex guitar_chords.tex   # twice, for references
```

To regenerate the staff notation and the theory chapter — after changing a
fingering, adding a chord, or editing the tables:

```bash
python3 outils/generer.py                      # .ly sources + theory_chapter.tex
lilypond -dcrop --formats=pdf gravures/*.ly    # engravings
pdflatex guitar_chords.tex                     # twice
```

### Why a generator

The staff notation under each diagram is **derived from the fingering in
`guitar_chords.tex`**, not drawn separately. That matters: six diagrams once
sounded a different chord than their name — an `E`-shape barre fingered as an
`A` shape, a `Caug` with a foreign F — and because the notation was engraved
independently, nothing flagged the disagreement. Now it cannot happen: change a
fingering and its notation follows, or the generator fails.

Before writing anything, the generator also checks that every diagram — those
of the songs included — sounds exactly the chord it names: all of its notes and
no other, only the fifth being allowed to drop out, as in the `C7` x32310. The
check caught a `Dadd9` without its F♯, really a `Dsus2`, and a `Bdim` with an
A, really a `Bm7♭5`.

`outils/chords.py` holds the pitch model. A pitch there is a *(letter,
alteration)* pair rather than a semitone number, and each chord tone gets its
letter from the scale degree it occupies. That is what makes `Edim7` come out as
E–B♭–E–G–D♭ rather than E–A♯–E–G–C♯: a diminished seventh is a seventh, not a
sixth, and only the spelling says so.

`theory_chapter.tex` is generated from the same model. Its 98 rows differ only by
root and quality, and their commentary is a template with the key's own note
names filled in — writing them out by hand would have been 98 chances to name the
wrong note.

### Dependencies

- LaTeX: `tikz`, `geometry`, `xcolor`, `titlesec`, `fancyhdr`, `booktabs`,
  `longtable`, `mdframed`, `colortbl`, `array`, `graphicx`
- LilyPond 2.24 or later (only to regenerate the engravings)
- Python 3 (standard library only)

## License

This project is licensed under the [MIT License](LICENSE).

---
Copyright (c) 2026 Fabian Bastin
