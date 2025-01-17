import numpy as np
from charcade import color

class Fretboard:
    """
    Class for assembling the fretboard
    """
    def __init__(self, tuning=None, fret_amount=25):
        if tuning is None:
            tuning = ['E', 'A', 'D', 'G', 'B', 'E']
        self.tuning = tuning
        self.fret_amount = fret_amount

        # Modular arithmetic is used to loop over this list and encode each string based on its tuning into a dict
        self.notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

        # Encoded fretboard. Using np for easy transposing
        self.fretboard = np.array([[(6 * (f - 1) + i) for i in range(1, 7)] for f in range(1, fret_amount + 1)])
        self.encoded_fretboard = {}
        self.constructed_fretboard = None
        self.encode_fretboard()
        self.assemble_encoded_fretboard()

        # Fret limit. Sets the amount of frets that can be looked at to find each chord.
        # This ensures that chords are possible to play

    def encode_fretboard(self):
        # Uses tuning to encode each string for the note that it will be on each fret.
        # Returns a dictionary where the number is the key and the note is the value.
        # Strings are transposed so each string is in its own list rather than the first value of each list.
        transposed_strings = [list(string) for string in self.fretboard.T]
        for string_index, note in enumerate(self.tuning):
            string = transposed_strings[string_index]
            for fret_index, fret_position in enumerate(string):
                self.encoded_fretboard[fret_position] = self.notes[(self.notes.index(note) + fret_index) % 12]

    def assemble_encoded_fretboard(self):
        self.constructed_fretboard = [[(self.encoded_fretboard.get(num), num) for num in row]for row in self.fretboard]


class Chord:
    """
    Class for assembling the tabs for each chord
    """

    def __init__(self, chord, fret_instance):
        self.chord = chord
        self.fretboard = fret_instance # Instance of the generated fretboard

        # Sets fret limit that the chord is searched within
        self.fret_limit = list(range(4))

        # Symbols to generate tab output
        self.no_strum = 'X'
        self.string = color('┃ ', 'purple40')
        self.finger = color('● ', 'green80')
        self.fret_splitter = color('╋━━╋━━╋━━╋━━╋━━╋', 'purple40')
        self.top_bottom = '━━━━━━━━━━━━━━━━'

        self.tabs = [] # Stores generated tabs

    # Checks if down strum on chord is sequential
    @staticmethod
    def is_sequential(numbers):
        return all(numbers[i] + 1 == numbers[i + 1] for i in range(len(numbers) - 1))

    def find_chords(self):
        """
        Separates fretboard into intervals based on fret_limit starting at the 1st fret to nth then 2nd to nth
        Searches for root note within the range of frets and then each other note within the chord
        """

        # Stores all numbers where each note from the chord is found.
        # Used for replacing the numbers on the number encoded fretboard
        while self.fret_limit[-1] < self.fretboard.fret_amount:
            # Tracks string numbers to make sure that strings aren't skipped on a chord
            # If string numbers aren't sequential the loop is broken and the fret position is moved up by 1
            string_tracking = []

            # For checking strings that have already been fretted using the string index
            used_strings = []

            current_frets = [self.fretboard.constructed_fretboard[num] for num in self.fret_limit]
            note_numbers = [[note[1] for note in inner_list] for inner_list in current_frets]
            chord = []
            chord_notes = []
            for note in self.chord:
                for string, fret in enumerate(current_frets):
                    for index, finger in enumerate(fret):
                        if note == finger[0] and index not in used_strings:
                            chord.append(finger[1])
                            chord_notes.append((finger[0], index))
                            used_strings.append(index)
                            continue
                    string_tracking.append(string)
            tab = []
            for fret in note_numbers:
                fret_tab = []
                for note in fret:
                    if note in chord:
                        fret_tab.append(self.finger)
                    else:
                        fret_tab.append(self.string)
                tab.append(fret_tab)
                tab.append([self.fret_splitter])
            used_strings.sort()
            if self.is_sequential(used_strings):
                notes_on_fret = '  '.join([note[0] for note in sorted(chord_notes, key=lambda x: x[1])])
                tab = tab[1:]
                top_bar = [self.top_bottom[len(str(self.fret_limit[0])) + 1:], self.fret_limit[0] + 1]
                tab.insert(0, top_bar)
                tab.insert(0, [notes_on_fret])
                tab.append([self.top_bottom])
                self.tabs.append(tab)
            self.fret_limit = [fret + 1 for fret in self.fret_limit]

    # Shows tabs in terminal for debugging
    def show_tabs(self):
        fret_len = len(self.tabs[0])
        for i in self.tabs:
            for n in i:
                print(*n)
            print()
        # Get the number of items in the longest list
        # Get the number of items in the longest list

        print(fret_len)
