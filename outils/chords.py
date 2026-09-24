#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèle des accords de guitare : doigtés, hauteurs, orthographe.

Source de vérité unique. Les portées gravées sous chaque diagramme sont
dérivées des doigtés lus dans `guitar_chords.tex` : la notation ne peut donc
pas contredire le diagramme qu'elle accompagne, ce qui est arrivé — six
diagrammes sonnaient un autre accord que leur nom, et leurs portées, gravées
séparément, ne le signalaient pas.

Une hauteur est ici un couple (lettre, altération), pas un numéro de demi-ton :
l'accord de la7 contient un sol naturel et non un fa double dièse, et seule
l'orthographe le dit.
"""

import re

# Cordes à vide, du mi grave au mi aigu, en numéros MIDI.
CORDES_MIDI = [40, 45, 50, 55, 59, 64]

LETTRES = "CDEFGAB"
DEMI_TONS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

# Qualités d'accord : intervalles en demi-tons depuis la fondamentale, et le
# degré d'échelle correspondant. Le degré fixe la *lettre*, l'intervalle fixe
# l'altération — c'est ce qui distingue une quinte diminuée d'une quarte
# augmentée, qui sonnent pareil.
QUALITES = {
    "":      [(0, 1), (4, 3), (7, 5)],
    "m":     [(0, 1), (3, 3), (7, 5)],
    "5":     [(0, 1), (7, 5)],
    "sus2":  [(0, 1), (2, 2), (7, 5)],
    "sus4":  [(0, 1), (5, 4), (7, 5)],
    "6":     [(0, 1), (4, 3), (7, 5), (9, 6)],
    "m6":    [(0, 1), (3, 3), (7, 5), (9, 6)],
    "add9":  [(0, 1), (2, 2), (4, 3), (7, 5)],
    "7":     [(0, 1), (4, 3), (7, 5), (10, 7)],
    "maj7":  [(0, 1), (4, 3), (7, 5), (11, 7)],
    "m7":    [(0, 1), (3, 3), (7, 5), (10, 7)],
    "aug":   [(0, 1), (4, 3), (8, 5)],
    "dim":   [(0, 1), (3, 3), (6, 5)],
    "dim7":  [(0, 1), (3, 3), (6, 5), (9, 7)],
    "m7b5":  [(0, 1), (3, 3), (6, 5), (10, 7)],
}


def lire_racine(txt):
    """« B$\\flat$m » -> (11, -1, 'm')."""
    t = (txt.replace("$\\flat$", "b").replace("$\\sharp$", "#")
            .replace("\\flat", "b").replace("\\sharp", "#")
            .replace(" major", "").replace(" minor", "m").strip())
    m = re.match(r"^([A-G])([b#]?)(.*)$", t)
    if not m:
        return None
    alt = 1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0
    qual = m.group(3).strip().replace("♭5", "b5")
    return m.group(1), alt, qual


def notes_accord(lettre, alt, qual):
    """
    Orthographe de chaque note de l'accord : {classe de hauteur: (lettre, alt)}.

    Le degré impose la lettre, l'intervalle impose l'altération. La septième
    diminuée d'un dim7 s'écrit donc double bémol, et non sixte majeure.
    """
    base = LETTRES.index(lettre)
    pc0 = (DEMI_TONS[lettre] + alt) % 12
    out = {}
    for demi, degre in QUALITES[qual]:
        l = LETTRES[(base + degre - 1) % 7]
        # Altération telle que la note tombe à l'intervalle voulu.
        ecart = (DEMI_TONS[l] - DEMI_TONS[lettre] - alt) % 12
        a = alt + ((demi - ecart + 6) % 12) - 6 if False else None
        # Calcul direct : différence entre le demi-ton visé et la note naturelle.
        vise = (pc0 + demi) % 12
        nat = DEMI_TONS[l]
        a = (vise - nat + 6) % 12 - 6
        out[vise] = (l, a)
    return out


def hauteurs(doigte):
    """Doigté [None|frette] par corde -> liste de numéros MIDI, du grave à l'aigu."""
    return [CORDES_MIDI[i] + f for i, f in enumerate(doigte) if f is not None]


def lily(midi, orthographe):
    """Note LilyPond, orthographiée selon l'accord."""
    pc = midi % 12
    if pc in orthographe:
        lettre, alt = orthographe[pc]
    else:
        # Note étrangère à l'accord : on retombe sur une écriture par défaut.
        lettre, alt = _defaut(pc)
    suff = {-2: "eses", -1: "es", 0: "", 1: "is", 2: "isis"}[alt]
    # Octave : celle de la *lettre*, pas celle du demi-ton — si dièse appartient
    # à l'octave du si qui le précède, pas à celle du do qui suit.
    oct_reelle = midi // 12 - 1
    pc_nat = DEMI_TONS[lettre]
    if pc_nat + alt >= 12:
        oct_reelle -= 1
    elif pc_nat + alt < 0:
        oct_reelle += 1
    marque = "'" * (oct_reelle - 3) if oct_reelle >= 3 else "," * (3 - oct_reelle)
    return lettre.lower() + suff + marque


def _defaut(pc):
    table = {0: ("C", 0), 1: ("C", 1), 2: ("D", 0), 3: ("E", -1), 4: ("E", 0),
             5: ("F", 0), 6: ("F", 1), 7: ("G", 0), 8: ("A", -1), 9: ("A", 0),
             10: ("B", -1), 11: ("B", 0)}
    return table[pc]
