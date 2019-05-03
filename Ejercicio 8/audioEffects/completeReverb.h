//completeReverb.h
#ifndef COMPLETEREVERB_H
#define COMPLETEREVERB_H
typedef float SAMPLE;

void completeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareCompleteReverb(void);
void refreshCompleteReverb(int var1, int var2, void * p2effect);

#endif