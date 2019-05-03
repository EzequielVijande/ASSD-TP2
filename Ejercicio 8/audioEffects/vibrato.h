//vibrato.h

#ifndef VIBRATO_H
#define VIBRATO_H
typedef float SAMPLE;

void vibratoCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareVibrato(void);
void refreshVibrato(int var1, int var2, void * p2effect);

#endif