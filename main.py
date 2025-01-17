from fret import Fretboard, Chord
fretboard = Fretboard()

chord = ['C', 'E', 'G']
tabs = Chord(chord, fretboard)
tabs.find_chords()
tabs.show_tabs()

