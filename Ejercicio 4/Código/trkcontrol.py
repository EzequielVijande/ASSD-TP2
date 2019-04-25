import midi
import wav_gen
import math


class TrackProcessor:
    def __init__(self, resolution):
        self.evs_dict = dict()
        self.evs_dict['Note On'] = self.handle_note_on
        self.evs_dict['Note Off'] = self.handle_note_off
        self.evs_dict['After Touch'] = None
        self.evs_dict['Control Change'] = None
        self.evs_dict['Program Change'] = None
        self.evs_dict['Channel After Touch'] = None
        self.evs_dict['Pitch Wheel'] = None
        self.evs_dict['SysEx'] = None
        self.evs_dict['Sequence Number'] = None
        self.evs_dict['Text'] = None
        self.evs_dict['Copyright Notice'] = None
        self.evs_dict['Track Name'] = self.handle_track_name
        self.evs_dict['Instrument Name'] = None
        self.evs_dict['Lyrics'] = None
        self.evs_dict['Marker'] = None
        self.evs_dict['Cue Point'] = None
        self.evs_dict['Program Name'] = None
        self.evs_dict['Channel Prefix'] = None
        self.evs_dict['Unknown'] = None
        self.evs_dict['MIDI Port/Cable'] = None
        self.evs_dict['Track Loop'] = None
        self.evs_dict['End of Track'] = self.handle_eot
        self.evs_dict['Set Tempo'] = self.handle_set_tempo
        self.evs_dict['SMPTE Offset'] = None
        self.evs_dict['Time Signature'] = None
        self.evs_dict['Key Signature'] = None
        self.evs_dict['Sequencer Specific'] = None

        # list of notes that are turned on after a NoteOnEvent and haven t been turned off by a NoteOffEvent
        # or the corresponding NoteOnEvent yet.
        self.on_notes = []
        # the initial bpm for the audio is set to 120 bpm by default. The tempo can be changed by a SetTempoEvent
        self.curr_bpm = 120
        # resolution used to convert ticks to time
        self.curr_resolution = resolution
        # buffer in which the samples used to generate the .wav file will be stored
        self.x_out = []
        # time in seconds of the last event
        self.last_ev_time = 0
        self.last_sent_time = 0

        self.frame_rate = 44100

        self.curr_track_name = ''
        self.output_info = None

    def process_track(self, track: midi.Track, name=''):
        self.output_info = None
        self.x_out = []
        self.on_notes = []
        self.curr_track_name = name
        for ev in track:
            self.last_ev_time += ev.tick * 60 / self.curr_bpm / self.curr_resolution
            if self.evs_dict[ev.name] is not None:  # looks for the handler of the specific event
                self.evs_dict[ev.name](ev)

        self.output_info = TrackInfo(self.on_notes, self.curr_track_name)
        return self.output_info

    def handle_track_name(self, ev: midi.TrackNameEvent):
        if self.curr_track_name == '':
            self.curr_track_name = ev.text

    def handle_note_on(self, ev: midi.NoteOnEvent):
        if ev.get_velocity() == 0:
            self.off_note(ev)
        else:
            self.on_notes.append([ev, self.last_ev_time])

    def handle_note_off(self, ev: midi.NoteOffEvent):
        self.off_note(ev)

    def handle_eot(self, ev: midi.EndOfTrackEvent):
        self.off_all_notes()

    def off_all_notes(self):
        off_ev = midi.NoteOnEvent()
        for i in range(len(self.on_notes)):
            if len(self.on_notes[i])==2:
                on_ev, on_time = self.on_notes[i]
                off_ev.set_pitch(on_ev.get_pitch())
                off_ev.set_velocity(0)
                self.off_note(off_ev)

    def handle_set_tempo(self, ev: midi.SetTempoEvent):
        self.curr_bpm = ev.bpm

    def off_note(self, off_ev: midi.NoteEvent):
        """Replaces the (NoteOnEvent,on_time) tuple in self.on_notes with
(NoteOnEvent, note duration)"""
        for i in range(len(self.on_notes)):
            if len(self.on_notes[i]) == 2:
                on_ev, ex_time = self.on_notes[i]
                if on_ev.get_pitch() == off_ev.get_pitch():
                    self.on_notes[i] = [on_ev, ex_time, self.last_ev_time - ex_time]


class TrackInfo:

    def __init__(self, notes, track_name):
        self.notes = notes
        self.track_name = track_name

    def get_total_notes(self):
        return len(self.notes)

    def get_note_at(self, i):
        return self.notes[i]

    def get_track_name(self):
        return self.track_name

    def get_all_notes_copy(self):
        return self.notes[:]
