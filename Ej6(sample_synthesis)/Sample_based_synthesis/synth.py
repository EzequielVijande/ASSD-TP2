import midi
import wav_gen
import math


class Synthesizer:

    def __init__(self):
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
        self.evs_dict['Track Name'] = None
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
        self.curr_resolution = -1
        # buffer in which the samples used to generate the .wav file will be stored
        self.x_out = []
        # time in seconds of the last event
        self.last_ev_time = 0
        self.last_sent_n = 0
        self.last_sent_time = 0
        # callback used to generate a note array with the corresponding synthesis method
        self.create_notes_callback = None
        # rate by which the samples will be outputted.
        self.frame_rate = 44100
        # manager used to generate the .wav file
        self.wav_manager = wav_gen.WaveManagement()
        self.avg_counter = 0
        # instrumento con el cual se va a interpretar el track
        self.instrument =''

    def set_resolution(self, resolution):
        """set_resolution should be called every time the pattern to be synthesized is changed!"""
        self.curr_resolution = resolution

    def set_create_notes_callback(self, callback):
        self.create_notes_callback = callback

    def synthesize(self, track: midi.Track):
        self.x_out = []
        i = 0
        for ev in track:
            i += 1
            segs_per_tick = 60 / self.curr_bpm / self.curr_resolution
            self.last_ev_time += ev.tick * segs_per_tick
            # print(ev.name + str(i))
            if self.evs_dict[ev.name] is not None:              # looks for the handler of the specific event
                self.evs_dict[ev.name](ev)

            if len(self.x_out) > 10**5:             # arbitrarily chosen length in which the buffer should be cleared
                self.refresh_notes()
                self.avg_counter = 0
                self.last_sent_n += len(self.x_out)-1       #
                self.wav_manager.generate_wav(False, self.x_out, file_name='Track1.wav') # generate part of the final .wav
                self.x_out = []         # clears the buffer
                self.avg_counter = 0
        if len(self.x_out) > 0:
            self.wav_manager.generate_wav(True, self.x_out, file_name='Track1.wav')

    def refresh_notes(self):
        back_up = self.on_notes[:]
        self.off_all_notes()
        self.last_sent_time += len(self.x_out) / self.frame_rate
        for j in range(len(back_up)):
            on_ev, on_time = back_up[j]
            back_up[j] = (on_ev, self.last_sent_time)
        self.on_notes = back_up

    def handle_note_on(self, ev: midi.NoteOnEvent):
        if ev.get_velocity() == 0:
            self.off_note(ev)
        else:
            self.on_notes.append((ev, self.last_ev_time))

    def handle_note_off(self, ev: midi.NoteOffEvent):
        self.off_note(ev)

    def handle_eot(self, ev: midi.EndOfTrackEvent):
        # off all notes, then end track
        self.off_all_notes()

    def off_all_notes(self):
        off_ev = midi.NoteOnEvent()

        for on_ev, on_time in self.on_notes:
            off_ev.set_pitch(on_ev.get_pitch())
            off_ev.set_velocity(0)
            self.off_note(off_ev)

    def handle_set_tempo(self, ev: midi.SetTempoEvent):
        self.curr_bpm = ev.bpm

    def off_note(self, off_ev: midi.NoteEvent):
        """off_ev is not necessarily a NoteOffEvent
It may also be a NoteOnEvent, hence the generic 'Event' annotation"""
        for on_ev, ex_time in self.on_notes:
            if on_ev.get_pitch() == off_ev.get_pitch():
                self.play_note((on_ev, ex_time), (off_ev, self.last_ev_time))
                self.on_notes.remove((on_ev, ex_time))

    def play_note(self, on_tuple, off_tuple):
        on_ev, on_time = on_tuple
        off_ev, off_time = off_tuple
        beginning_n = int(on_time*self.frame_rate) - self.last_sent_n
        ending_n = int(off_time*self.frame_rate)+1 - self.last_sent_n
        notes = self.create_notes_callback(on_ev.get_pitch(), ending_n-beginning_n,on_ev.get_velocity(),self.instrument)
        self.sum_note_arrays(notes, beginning_n, ending_n)

    def sum_note_arrays(self, notes: list, beginning_n: int, ending_n: int):
        """sums the new note to previous notes that are on the same time interval"""
        if len(self.x_out) < ending_n:
            self.x_out += [0]*(ending_n-len(self.x_out))
        for i in range(ending_n-beginning_n-1):
            self.x_out[i + beginning_n] = (self.x_out[i + beginning_n]*self.avg_counter + notes[i]) / (self.avg_counter+1)
            self.avg_counter += 1