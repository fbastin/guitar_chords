\version "2.24.3"
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
\score {
  \new Staff {
    \clef "treble_8"
    \key e \major
    \omit Staff.TimeSignature
    \cadenzaOn
    <e g b d'>1
    \bar "|."
  }
  \layout { }
}
