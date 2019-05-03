//convolutionReverb.c

#include "convolutionReverb.h"
#include "math.h"
#include "stdlib.h"
#include "fftC.h"
#include "hanning.h"

#define L 8000
#define FPB 64

typedef int EFFECT_TYPE;
typedef float SAMPLE;



typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
}reverbConvolution_t;


void * prepareConvolutionReverb(void){
    reverbConvolution_t * p;
    p = malloc(sizeof(reverbConvolution_t));

    return (void *) p;
}

void convolutionReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    
}

void refreshConvolutionReverb(int var1, int var2, void * p2effect){
    
}