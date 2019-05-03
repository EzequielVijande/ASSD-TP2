//flanger.h

#ifndef FLANGER_H
#define FLANGER_H

typedef float SAMPLE;
void flangerCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareFlanger(void);
void refreshFlanger(int var1, int var2, void * p2effect);

#endif