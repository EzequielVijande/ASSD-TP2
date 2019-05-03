//head3D.h
#ifndef HEAD3D_H
#define HEAD3D_H

typedef float SAMPLE;
void headPhones3DCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareHeadPhones3D(void);
void refreshHeadPhones3D(int var1, int var2, void * p2effect);

#endif