import midi
import wav_gen


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

        self.on_notes = []
        self.curr_bpm = 120
        self.curr_resolution = -1
        self.x_out = []
        self.last_ev_time = 0
        self.play_note_callback = None

    def set_resolution(self, resolution):
        """set_resolution should be called every time the pattern to be synthesized is changed!"""
        self.curr_resolution = resolution

    def set_play_note_callback(self, callback):
        self.play_note_callback = callback

    def synthesize(self, track: midi.Track):
        self.x_out = []
        for ev in track:
            microsegs_per_tick = 60 * 10 ** 6 / self.curr_bpm / self.curr_resolution
            self.last_ev_time += ev.tick * microsegs_per_tick
            if self.evs_dict[ev.name] is not None:
                self.evs_dict[ev.name](ev)

        wav_gen.generate_wav(self.x_out)

    def handle_note_on(self, ev: midi.NoteOnEvent):
        if ev.get_velocity() == 0:
            self.off_note(ev)
        else:
            self.on_notes.append((ev, self.last_ev_time))

    def handle_note_off(self, ev: midi.NoteOffEvent):
        self.off_note(ev)

    def handle_eot(self, ev: midi.EndOfTrackEvent):
        # off all notes, then end track
        # print('handled eot')
        pass

    def handle_set_tempo(self, ev: midi.SetTempoEvent):
        self.curr_bpm = ev.bpm

    def off_note(self, off_ev: midi.Event):
        """off_ev is not necessarily a NoteOffEvent
It may also be a NoteOnEvent, hence the generic 'Event' annotation"""
        for on_ev, ex_time in self.on_notes:
            if on_ev.get_pitch() == off_ev.get_pitch():
                self.play_note_callback((on_ev, ex_time), (off_ev, self.last_ev_time))


class FmSynthesizer(Synthesizer):
    def __init__(self):
        self.set_play_note_callback(self.play_note)
        super(FmSynthesizer, self).__init__()

    def play_note(self, on_tuple, off_tuple):
        on_ev, on_time = on_tuple
        off_ev, off_time = off_tuple
        print('note_played: ' + str(on_ev.get_pitch) + '.\n Played from ' + str(on_time) + 'microseg to ' + str(off_time) + ' microseg.')


# pruebas
synth = FmSynthesizer()
synth.set_play_note_callback(synth.play_note)
pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
synth.set_resolution(pattern.resolution)
for trk in pattern:
    synth.synthesize(trk)
