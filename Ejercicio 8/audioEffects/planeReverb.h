//planeReverb.h
#ifndef PLANEREVERB_H
#define PLANEREVERB_H

typedef float SAMPLE;

void planeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * preparePlaneReverb(void);
void refreshPlaneReverb(int var1, int var2, void * p2effect);

#endif