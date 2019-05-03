//allPassReverb.h
#ifndef ALLPASSREVERB_H
#define ALLPASSREVERB_H
typedef float SAMPLE;
void allPassReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareAllPassReverb(void);
void refreshAllPassReverb(int var1, int var2, void * p2effect);

#endif