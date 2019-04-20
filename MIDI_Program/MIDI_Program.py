import midi

pattern = midi.read_midifile(".\ArchivosMIDI\Super Mario 64 - Bob-Omb Battlefield.mid")
ev_name= (pattern[2][10]).name
print (ev_name)

