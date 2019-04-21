import midi
import wav_gen
import math
import random

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
        self.frame_rate = 44100

    def set_resolution(self, resolution):
        """set_resolution should be called every time the pattern to be synthesized is changed!"""
        self.curr_resolution = resolution

    def set_play_note_callback(self, callback):
        self.play_note_callback = callback

    def synthesize(self, track: midi.Track):
        self.x_out = []
        i = 0
        for ev in track:
            i += 1
            segs_per_tick = 60 / self.curr_bpm / self.curr_resolution
            self.last_ev_time += ev.tick * segs_per_tick
            print(ev.name + str(i))
            if self.evs_dict[ev.name] is not None:
                self.evs_dict[ev.name](ev)
            print(len(self.x_out))
            if len(self.x_out) > 10**5:
                wav_gen.generate_wav(self.x_out)
                self.x_out = []
        print('Salio')
        if len(self.x_out) > 0:
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
                self.on_notes.remove((on_ev, ex_time))

class FmSynthesizer(Synthesizer):
    def __init__(self):
        self.set_play_note_callback(self.play_note)
        super(FmSynthesizer, self).__init__()

    def play_note(self, on_tuple, off_tuple):
        on_ev, on_time = on_tuple
        off_ev, off_time = off_tuple
        #print('note_played: ' + str(on_ev.get_pitch) + '.\n Played from ' + str(on_time) + 'microseg to ' + str(off_time) + ' microseg.')
        beginning_n = int(on_time*self.frame_rate)
        ending_n = int(off_time*self.frame_rate)+1
        notes = self.create_note_array(on_ev.get_pitch(), ending_n-beginning_n)
        self.sum_note_arrays(notes, beginning_n, ending_n)

    def sum_note_arrays(self, notes: list, beginning_n: int, ending_n: int):
        if ending_n > len(self.x_out):
            self.x_out += [0]*(ending_n-len(self.x_out))
        for i in range(beginning_n, ending_n):
            self.x_out[i] += notes[i-beginning_n]

    def create_note_array(self, pitch, amount_of_ns: int):
        notes = []
        freq = random.randint(1, 101)*20
        for i in range(amount_of_ns):
            notes.append(math.cos(2*math.pi*400*i/self.frame_rate))
        print('len_notes: ' + str(len(notes)))
        return notes

    #def pitch_2_freq(self,pitch):
        #return freq

# pruebas
synth = FmSynthesizer()
synth.set_play_note_callback(synth.play_note)
pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
synth.set_resolution(pattern.resolution)
#for trk in pattern:
    #synth.synthesize(trk)
synth.synthesize(pattern[1])
