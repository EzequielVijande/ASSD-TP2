//lowPassReverb.h

#ifndef LOWPASSREVERB_H
#define LOWPASSREVERB_H

typedef float SAMPLE;
void lowPassReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareLowPassReverb(void);
void refreshLowPassReverb(int var1, int var2, void * p2effect);

#endif