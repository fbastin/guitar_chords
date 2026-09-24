#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Produit les portées gravées du guide, à partir des doigtés du document.

    python3 outils/generer.py

Les doigtés sont lus dans `guitar_chords.tex` : chaque portée montre donc
exactement ce que sonne le diagramme qu'elle accompagne. Les graver à part,
comme c'était le cas, laisse les deux diverger sans que rien ne le signale.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chords import hauteurs, lily, lire_racine, notes_accord

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(RACINE, "guitar_chords.tex")
DIR_LY = os.path.join(RACINE, "gravures")

PREAMBULE = r"""\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
#(set-global-staff-size 15)
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
"""


def doigte_depuis(depart, marques, barres, points):
    """Frette effective de chaque corde ; None si étouffée, 0 si à vide."""
    f = [None] * 6
    vues = set()
    for tok in filter(None, (x.strip() for x in marques.split(","))):
        s, t = tok.split("/")
        s = int(s)
        vues.add(s)
        f[s - 1] = None if t == "x" else 0
    for tok in filter(None, (x.strip() for x in barres.split(","))):
        lo, hi, fr = (int(x) for x in tok.split("/"))
        for s in range(lo, hi + 1):
            if s not in vues:
                f[s - 1] = depart - 1 + fr
    for tok in filter(None, (x.strip() for x in points.split(","))):
        s, fr = (int(x) for x in tok.split("/"))
        f[s - 1] = depart - 1 + int(fr)
    return f


MOTIF = re.compile(
    r"\\cw\{([^}]*)\}\{\\chord\{((?:[^{}]|\{[^{}]*\})*)\}"
    r"\{(\d+)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\}")


def lire_accords():
    """Les accords du document : clef de fichier -> (nom affiché, doigté)."""
    src = open(TEX, encoding="utf-8").read()
    out = {}
    for m in MOTIF.finditer(src):
        clef, nom, dep, mar, bar, pts = m.groups()
        out[clef] = (nom, doigte_depuis(int(dep), mar, bar, pts))
    return out


def portee(nom, doigte):
    """
    Le voicing tel qu'il sonne, en rondes, sur portée en clé de sol octaviée.

    Pas d'armure : ces portées accompagnent un diagramme isolé, hors contexte
    tonal, et chaque altération doit donc se lire sur place.
    """
    r = lire_racine(nom)
    orth = notes_accord(*r) if r else {}
    notes = " ".join(lily(m, orth) for m in hauteurs(doigte))
    return r"""\score {
  \new Staff {
    \clef "treble_8"
    \omit Staff.TimeSignature
    \cadenzaOn
    <%s>1
    \bar "|."
  }
  \layout { }
}
""" % notes


# ---------------------------------------------------------------------------
# Chapitre de théorie : les sept familles
# ---------------------------------------------------------------------------
# Ordre des qualités dans chaque tableau, avec le nom complet, la formule et le
# gabarit de commentaire. Le commentaire est un gabarit et non un texte figé :
# il ne varie d'une famille à l'autre que par les noms de notes, que le modèle
# sait calculer. Transcrire les 98 lignes à la main aurait été 98 occasions de
# se tromper de note.
FAMILLE_ORDRE = [
    ("",      "major",         "1 -- 3 -- 5",                   "Bright, stable."),
    ("m",     "minor",         "1 -- $\\flat$3 -- 5",           "Dark. Lower the 3rd: {d3} $\\to$ $\\flat${d3}."),
    ("5",     "power chord",   "1 -- 5",                        "Raw, neutral. No 3rd."),
    ("sus2",  "sus. 2nd",      "1 -- 2 -- 5",                   "Open. Replace 3rd with 2nd ({d2})."),
    ("sus4",  "sus. 4th",      "1 -- 4 -- 5",                   "Tense. Replace 3rd with 4th ({d4})."),
    ("6",     "major sixth",   "1 -- 3 -- 5 -- 6",              "Sweet, vintage. Add 6th ({d6})."),
    ("add9",  "add nine",      "1 -- 3 -- 5 -- 9",              "Colourful. Add 2nd/9th ({d2}), no 7th."),
    ("7",     "dominant 7th",  "1 -- 3 -- 5 -- $\\flat$7",      "Bluesy. Lower 7th: {d7} $\\to$ $\\flat${d7}."),
    ("maj7",  "major 7th",     "1 -- 3 -- 5 -- 7",              "Dreamy, jazzy. Keep natural 7th ({d7})."),
    ("m7",    "minor 7th",     "1 -- $\\flat$3 -- 5 -- $\\flat$7", "Mellow, soulful. Lower 3rd and 7th."),
    ("aug",   "augmented",     "1 -- 3 -- $\\sharp$5",          "Eerie. Raise the 5th by 1 semitone."),
    ("dim",   "diminished",    "1 -- $\\flat$3 -- $\\flat$5",   "Very tense. Lower 3rd and 5th."),
    ("dim7",  "dim. 7th",      "1 -- $\\flat$3 -- $\\flat$5 -- $\\flat\\flat$7", "Max. tense. All minor 3rds."),
    ("m7b5",  "half-dim.",     "1 -- $\\flat$3 -- $\\flat$5 -- $\\flat$7", "Tense, jazzy (also: {r}$\\varnothing$)."),
]

# Les sept fondamentales naturelles et leur armure.
FAMILLES = [("A", 3), ("B", 5), ("C", 0), ("D", 2), ("E", 4), ("F", -1), ("G", 1)]

ORDRE_DIESES = "FCGDAEB"
ORDRE_BEMOLS = "BEADGCF"
NOMBRES = {0: "no", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
           6: "six", 7: "seven"}


def gamme_majeure(lettre):
    """Les sept degrés de la gamme majeure, orthographiés."""
    from chords import DEMI_TONS, LETTRES
    base = LETTRES.index(lettre)
    pc = DEMI_TONS[lettre]
    pas = [0, 2, 4, 5, 7, 9, 11]
    out = []
    for i, demi in enumerate(pas):
        l = LETTRES[(base + i) % 7]
        vise = (pc + demi) % 12
        alt = (vise - DEMI_TONS[l] + 6) % 12 - 6
        out.append((l, alt))
    return out


def tex_note(l, alt):
    return l + ("$\\sharp$" if alt == 1 else "$\\flat$" if alt == -1 else "")


def armure_phrase(k):
    if k == 0:
        return "no sharps or flats"
    lettres = [ORDRE_DIESES[i] for i in range(k)] if k > 0 else \
              [ORDRE_BEMOLS[i] for i in range(-k)]
    signe = "$\\sharp$" if k > 0 else "$\\flat$"
    noms = ", ".join(x + signe for x in lettres)
    mot = "sharp" if k > 0 else "flat"
    return f"{NOMBRES[abs(k)]} {mot}{'s' if abs(k) > 1 else ''}: {noms}"


def ecrire_theorie():
    """Le chapitre, et les gravures qu'il appelle."""
    from chords import DEMI_TONS, LETTRES, QUALITES, notes_accord
    os.makedirs(DIR_LY, exist_ok=True)
    lignes = ["%% Produit par outils/generer.py — ne pas modifier à la main.", ""]
    n_grav = 0

    for lettre, armure in FAMILLES:
        degres = gamme_majeure(lettre)
        lignes.append(r"\subsection*{The %s Family}" % lettre)
        lignes.append(r"\noindent\textbf{Key signature:} %s.\smallskip" % armure_phrase(armure))
        lignes.append("")
        # La gamme, gravée, avec ses degrés sous la portée.
        nom_g = f"scale-{lettre}"
        _ecrire_ly(nom_g, _ly_gamme(degres, armure))
        n_grav += 1
        lignes.append(r"\begin{center}")
        lignes.append(r"\includegraphics[height=1.15cm]{%s.cropped}\\[2pt]" % nom_g)
        lignes.append(r"{\small\color{mygray}" +
                      r"\quad ".join(f"\\textbf{{{i+1}}} {tex_note(*d)}"
                                     for i, d in enumerate(degres)) +
                      r"\quad \textbf{8} " + tex_note(*degres[0]) + "}")
        lignes.append(r"\end{center}")
        lignes.append("")
        lignes.append(r"\begin{longtable}{@{}l l l c >{\raggedright\arraybackslash}p{4.4cm}@{}}")
        lignes.append(r"\toprule")
        lignes.append(r"\textbf{Symbol} & \textbf{Full name} & \textbf{Formula} & "
                      r"\textbf{Staff} & \textbf{Colour / use} \\")
        lignes.append(r"\midrule\endhead")
        for i_q, (qual, plein, formule, gabarit) in enumerate(FAMILLE_ORDRE):
            sym = lettre + (qual.replace("b5", "$\\flat$5") if qual else "")
            nom_ly = f"th-{lettre}{qual or 'maj'}"
            _ecrire_ly(nom_ly, _ly_accord(lettre, qual, armure))
            n_grav += 1
            texte = gabarit.format(
                r=lettre,
                d2=tex_note(*degres[1]), d3=tex_note(*degres[2]),
                d4=tex_note(*degres[3]), d6=tex_note(*degres[5]),
                d7=tex_note(*degres[6]))
            # Rayage une ligne sur deux, comme dans les tableaux voisins du guide.
            lignes.append(r"\rowcolor{%s}" % ("rowA" if i_q % 2 == 0 else "rowB"))
            lignes.append(
                r"\textbf{%s} & %s %s & %s & "
                r"\includegraphics[height=1.15cm]{%s.cropped} & %s \\"
                % (sym, lettre, plein, formule, nom_ly, texte))
        lignes.append(r"\bottomrule")
        lignes.append(r"\end{longtable}")
        lignes.append("")

    chemin = os.path.join(RACINE, "theory_chapter.tex")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    return chemin, n_grav


def _ecrire_ly(nom, corps):
    with open(os.path.join(DIR_LY, nom + ".ly"), "w", encoding="utf-8") as f:
        f.write(PREAMBULE + corps)


def _ly_note(l, alt, octave):
    suff = {-2: "eses", -1: "es", 0: "", 1: "is", 2: "isis"}[alt]
    marque = "'" * (octave - 3) if octave >= 3 else "," * (3 - octave)
    return l.lower() + suff + marque


def _ly_gamme(degres, armure):
    from chords import DEMI_TONS, LETTRES
    notes = []
    oct_ = 3
    prec = None
    for l, alt in degres + [degres[0]]:
        i = LETTRES.index(l)
        if prec is not None and i <= prec:
            oct_ += 1
        prec = i
        notes.append(_ly_note(l, alt, oct_))
    return r"""\score {
  \new Staff {
    \clef "treble_8"
    \key %s \major
    \omit Staff.TimeSignature
    \cadenzaOn
    %s
    \bar "|."
  }
  \layout { }
}
""" % (_ly_note(degres[0][0], degres[0][1], 3).rstrip("',"), " ".join(notes))


def _ly_accord(lettre, qual, armure):
    """L'accord en position serrée, empilé depuis la fondamentale."""
    from chords import DEMI_TONS, LETTRES, QUALITES, notes_accord
    alt0 = 0
    orth = notes_accord(lettre, alt0, qual)
    base_pc = DEMI_TONS[lettre]
    notes = []
    oct_ = 3
    prec = None
    for demi, degre in QUALITES[qual]:
        pc = (base_pc + demi) % 12
        l, a = orth[pc]
        i = LETTRES.index(l)
        if prec is not None and i <= prec:
            oct_ += 1
        prec = i
        notes.append(_ly_note(l, a, oct_))
    return r"""\score {
  \new Staff {
    \clef "treble_8"
    \key %s \major
    \omit Staff.TimeSignature
    \cadenzaOn
    <%s>1
    \bar "|."
  }
  \layout { }
}
""" % (lettre.lower(), " ".join(notes))


def main():
    os.makedirs(DIR_LY, exist_ok=True)
    accords = lire_accords()
    for clef, (nom, doigte) in sorted(accords.items()):
        chemin = os.path.join(DIR_LY, clef + "_t.ly")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(PREAMBULE + portee(nom, doigte))
    print(f"{len(accords)} portées de doigté écrites dans gravures/")
    chemin, n = ecrire_theorie()
    print(f"{n} portées de théorie écrites dans gravures/")
    print(f"chapitre : {os.path.relpath(chemin, RACINE)}")
    return accords


if __name__ == "__main__":
    main()
