import midi
import wave


class FmSynthesizer:

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
        self.evs_dict['Set Tempo'] = None
        self.evs_dict['SMPTE Offset'] = None
        self.evs_dict['Time Signature'] = None
        self.evs_dict['Key Signature'] = None
        self.evs_dict['Sequencer Specific'] = None

    def synthesize(self, track: midi.Track):
        for ev in track:
            if self.evs_dict[ev.name] is not None:
                self.evs_dict[ev.name]()

        self.generate_fm_wav()

    def handle_note_on(self, ev:midi.NoteOnEvent):
        pitch = ev.get_pitch()
        vel = ev.get_velocity()
        ev.length
        print('handled note on')

    def handle_note_off(self):
        print('handled note off')

    def handle_eot(self):
        print('handled eot')

    def generate_fm_wav(self):
        pass

    def generate_fm_wav(self):
        pass

# pruebas
synth = FmSynthesizer()
pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
for trk in pattern:
    synth.synthesize(trk)


