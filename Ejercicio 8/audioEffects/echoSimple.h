//echoSimple.h
#ifndef ECHOSIMPLE_H
#define ECHOSIMPLE_H
typedef float SAMPLE;
void echoSimpleCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareEchoSimple(void);
void refreshEchoSimple(int var1, int var2, void * p2effect);

#endif