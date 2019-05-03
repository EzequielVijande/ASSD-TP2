//robotizaion.h
#ifndef ROBOTIZATION_H
#define ROBOTIZATION_H
typedef float SAMPLE;

void robotizationCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareRobotization(void);
void refreshRobotization(int var1, int var2, void * p2effect);
#endif