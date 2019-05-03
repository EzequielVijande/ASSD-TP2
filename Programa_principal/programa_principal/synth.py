import midi
import wav_gen
import math

#Strings que indican el instrumento
GUITAR = "guitar"
ELECTRIC_GUITAR = "electric guitar"
DRUMS = "drums"
CORN_ANGLAIS = "corn anglais"
VIOLIN = "violin"
SAXO = "saxophone"
TRUMPET = "trumpet"
CLARINET = "clarinet"
BELL = "bell"

class Synthesizer:

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
        self.last_sent_n = 0
        # callback used to generate a note array with the corresponding synthesis method
        self.create_notes_callback = None
        # rate by which the samples will be outputted.
        self.frame_rate = 44100
        # manager used to generate the .wav file
        self.wav_manager = wav_gen.WaveManagement()
        self.avg_counter = 0
        self.curr_instrument = ''
        self.curr_track_name = ''
        self.aux_buffer_flag = False
        self.track_index = 0
        self.aux_buffer_size = 0
        self.set_tempo_ev = False
        self.tempo_map = None

    def set_create_notes_callback(self, callback):
        self.create_notes_callback = callback

    def synthesize(self, track: midi.Track, instrument: str, first_time: bool=False, n_frames: int=100000):
        # print('synth tempo_map'+ str(self.tempo_map))
        # print(self.curr_bpm)
        if first_time:
            self.x_out = []
            self.avg_counter = 0
            self.last_ev_time = 0
            self.last_sent_n = 0
            self.on_notes = []
            self.curr_bpm = 120
            self.curr_track_name = ''
            self.aux_buffer_flag = False
            self.aux_buffer_size = 0
            self.track_index = 0
            self.set_tempo_ev = False

        self.curr_instrument = instrument

        i = 0
        for k in range(self.track_index, len(track)):
            ev = track[k]
            i += 1
            segs_per_tick = 60.0 / (self.curr_bpm * self.curr_resolution)
            self.last_ev_time += ev.tick * segs_per_tick
            self.update_tempo_if_tempo_map()

            if self.evs_dict[ev.name] is not None:              # looks for the handler of the specific event
                self.evs_dict[ev.name](ev)

            if (len(self.x_out) > n_frames)and(len(self.on_notes)==0):               # arbitrarily chosen length in which the buffer should be cleared
                self.avg_counter = 0
                returnable = self.x_out[0:n_frames]
                self.x_out = self.x_out[n_frames:]
                self.last_sent_n += len(returnable)-1
                self.aux_buffer_flag = True
                self.aux_buffer_size = len(self.x_out)
                self.avg_counter = 0
                self.track_index = k+1
                return returnable, False

        # the deletion of the tempo_map should come after fully synthesizing the track
        self.tempo_map = None
        if len(self.x_out) > n_frames:
            returnable = self.x_out[0:n_frames]
            self.x_out = self.x_out[n_frames:]
            return returnable, False
        else:
            returnable = self.x_out + [0]*(n_frames-len(self.x_out)) #Lleno con ceros para devolver n_frames
            return returnable, True

    def handle_track_name(self, ev: midi.TrackNameEvent):
        if self.curr_track_name != '':
            self.curr_track_name = ev.text

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
        self.curr_bpm = ev.get_bpm()

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
        on_ev_tick = on_ev.tick
        off_ev_tick = off_ev.tick
        if(on_ev_tick < off_ev_tick): #Ignora el evento si las duraciones no tiene sentido
            beginning_n = int(on_time*self.frame_rate) - self.last_sent_n
            ending_n = int(off_time*self.frame_rate)+1 - self.last_sent_n
            notes = self.create_notes_callback(on_ev.get_pitch(), ending_n-beginning_n, on_ev.get_velocity(), self.curr_instrument)
            self.sum_note_arrays(notes, beginning_n, ending_n)

    def sum_note_arrays(self, notes: list, beginning_n: int, ending_n: int):
        """sums the new note to previous notes that are on the same time interval"""

        if len(self.x_out) < ending_n:
            self.x_out += [0]*(ending_n-len(self.x_out))
        avged = False
        for i in range(ending_n-beginning_n):
            if self.x_out[i + beginning_n] != 0:
                avged = True
                self.x_out[i + beginning_n] = (self.x_out[i + beginning_n]*self.avg_counter + notes[i]) / (self.avg_counter+1)
            else:
                self.x_out[i + beginning_n] = (self.x_out[i + beginning_n] + notes[i])
        if avged:
            self.avg_counter += 1

    def set_tempo_map(self, tempo_map):
        self.tempo_map = tempo_map[:]

    def get_tempo_map(self, track: midi.Track):
        last_ev_time = 0
        curr_bpm = 120
        self.tempo_map = []
        for ev in track:
            if ev.name == 'Set Tempo':
                curr_bpm = ev.get_bpm()
                self.curr_bpm = curr_bpm
                segs_per_tick = 60.0 / (self.curr_bpm * self.curr_resolution)
                last_ev_time += ev.tick * segs_per_tick
                self.tempo_map.append((last_ev_time, curr_bpm))
        # no set Tempo events found in this file !
        if len(self.tempo_map) == 0:
            self.tempo_map = None

        return self.tempo_map

    def update_tempo_if_tempo_map(self):
        if self.tempo_map is not None:
            if len(self.tempo_map) > 0:
                set_time, bpm = self.tempo_map[0]
                #print('set_time = ' + str(set_time))
                #print('last_ev_time = ' + str(self.last_ev_time))
                if set_time == 0:
                    self.curr_bpm = bpm
                    self.tempo_map = self.tempo_map[1:]
                elif set_time <= self.last_ev_time:
                    self.curr_bpm = bpm
                    print('set_time = ' + str(set_time))
                    print('bpm = '+ str(self.curr_bpm))
                    self.tempo_map = self.tempo_map[1:]
