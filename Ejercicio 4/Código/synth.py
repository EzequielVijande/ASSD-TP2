from trkcontrol import TrackInfo
import midi


class Synthesizer:

    def __init__(self, frame_rate):
        # callback used to generate a note array with the corresponding synthesis method
        self.create_notes_callback = None
        self.avg_counter = 0

        # rate by which the samples will be outputted.
        self.frame_rate = frame_rate
        self.x_out = []
        self.aux_buffer = []
        self.last_completed_tick = 0
        self.notes_to_send = []
        self.unplayed_notes = []
        self.on_notes = []
        self.last_sent_n = 0
        self.last_sent_time = 0
        self.curr_track_notes = None

    def synthesize(self, trk_info: TrackInfo, instrument: int, n_frames: int, first_time: bool):
        self.x_out.clear()
        self.avg_counter = 0
        if first_time:
            self.curr_track_notes = trk_info.get_all_notes_copy()

        if len(self.aux_buffer) > 0:                        # aux_buffer has some content to be sent
            self.x_out += self.aux_buffer[0:n_frames]
            self.aux_buffer = self.aux_buffer[n_frames:]

        # in case the buffer had some content copied to the x_out vector,
        # i should check if the x_out vector has reached its limit before continuing
        if len(self.x_out) < n_frames:
            for i in range(trk_info.get_total_notes()):
                on_ev, on_time, duration = self.curr_track_notes[i]
                # if the x_out vector has reached its maximum limit (the buffer has length >0)
                # in the previous iteration
                # and the new note starts after the last recorded time, then the iteration should stop
                # and the x_out vector should be sent (the excess has already been copied in aux_buffer).
                if on_time > (self.last_sent_n / self.frame_rate) and len(self.aux_buffer) > 0:
                    break
                pitch = on_ev.get_pitch()
                velocity = on_ev.get_velocity()
                beginning_n = int(on_time * self.frame_rate) - self.last_sent_n
                ending_n = int((on_time+duration) * self.frame_rate) + 1 - self.last_sent_n
                notes = self.create_notes_callback(pitch, ending_n-beginning_n, velocity, instrument)
                # sum_note_arrays should average between notes played at the same time on the track!
                self.sum_note_arrays(notes, beginning_n, ending_n)

                # the x_out vector has reached its limit!!
                # the aux_buffer should be filled with all the notes playing but t
                if len(self.x_out) > n_frames:
                    self.curr_track_notes.remove((on_ev, on_time, duration))
                    self.refresh_notes(trk_info)
                    self.avg_counter = 0
                    self.last_sent_n += len(self.x_out) - 1
                    self.aux_buffer = self.x_out[n_frames:]
                    self.x_out = self.x_out[0:n_frames]
                if len(self.aux_buffer) > 0:
                    try:
                        self.curr_track_notes.remove((on_ev, on_time, duration))
                    except ValueError:
                        pass

        return self.x_out

    def sum_note_arrays(self, notes: list, beginning_n: int, ending_n: int):
        """sums the new note to previous notes that are on the same time interval"""
        if len(self.x_out) < ending_n:
            self.x_out += [0] * (ending_n - len(self.x_out))
        avged = False
        for i in range(ending_n - beginning_n):
            if self.x_out[i + beginning_n] != 0:
                avged = True
                self.x_out[i + beginning_n] = (self.x_out[i + beginning_n] * self.avg_counter + notes[i]) / (
                            self.avg_counter + 1)
            else:
                self.x_out[i + beginning_n] = (self.x_out[i + beginning_n] + notes[i])
            # print(self.avg_counter)
        if avged:
            self.avg_counter += 1

    def refresh_notes(self, trk_info: TrackInfo):
        for on_ev, on_time, duration in range(trk_info.get_total_notes()):
            pass
        self.off_all_notes()
        self.last_sent_time += len(self.x_out) / self.frame_rate
        for j in range(len(back_up)):
            on_ev, on_time = back_up[j]
            back_up[j] = (on_ev, self.last_sent_time)
        self.on_notes = back_up

    def set_create_notes_callback(self, callback):
        self.create_notes_callback = callback

    def set_frame_rate(self, frame_rate):
        self.frame_rate = frame_rate

    def off_all_notes(self):
        off_ev = midi.NoteOnEvent()

        for on_ev, on_time in self.on_notes:
            off_ev.set_pitch(on_ev.get_pitch())
            off_ev.set_velocity(0)
            self.off_note(off_ev)

    def off_note(self, off_ev: midi.NoteEvent):
        """off_ev is not necessarily a NoteOffEvent
It may also be a NoteOnEvent, hence the generic 'Event' annotation"""
        for on_ev, ex_time in self.on_notes:
            if on_ev.get_pitch() == off_ev.get_pitch():
                self.on_notes.remove((on_ev, ex_time))