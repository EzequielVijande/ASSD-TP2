//convolutionReverb.h

#ifndef CONVOLUTIONREVERB_H
#define CONVOLUTIONREVERB_H
typedef float SAMPLE;
void convolutionReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void * prepareConvolutionReverb(void);
void refreshConvolutionReverb(int var1, int var2, void * p2effect);

#endif