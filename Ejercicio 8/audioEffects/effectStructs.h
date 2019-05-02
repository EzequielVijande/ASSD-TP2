//effectStructs.h
//This file contain the structures of the audio effects, having into account the parameters
//that define the caracteristics of each one.

#ifndef EFFECTSTRUCTS_H
#define EFFECTSTRUCTS_H

//EFFECTS AVAILABLE FOR THE USER:
#define REVERB_ALLPASS 0 //primer efecto
#define ECHO_SIMPLE 1
#define REVERB_PLANE 2
#define REVERB_LOWPASS 3
#define REVERB_COMPLETE 4
#define REVERB_CONVOLUTION 5
#define ROBOTIZATION 6
#define HEADPHONES3D 7
#define VIBRATO 8
#define FLANGER 9     //ultimo efecto


#define L 20000
#define FPB 512





typedef int EFFECT_TYPE;
typedef float SAMPLE;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
    int n;
}echoSimple_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
    float memoryOutputsDer[L];
    float memoryOutputsIzq[L];
    int n;
}reverbPlane_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
    float memoryOutputsDer[L];
    float memoryOutputsIzq[L];
    int n;
}reverbAllPass_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
}reverbLowPass_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
}reverbConvolution_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
}reverbComplete_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
    float memDerOLADer[FPB];
    float memDerOLAIzqFFT[FPB];
    float memIzqOLADer[FPB];
    float memIzqOLAIzqFFT[FPB];
    float memDerFFTnoOLA[FPB];
    float memIzqFFTnoOLA[FPB];
    float hanning[FPB];
    int flag;
}robotization_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
}headPhones3D_t;


typedef struct{
    int maxDelay;           //comentar que representan estos parámetros
    int minDelay;
    int freq;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
    float memoryOutputsDer[L];
    float memoryOutputsIzq[L];
    int n;
    
}vibrato_t;

typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
    int n;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
}flanger_t;

typedef struct {
    
    
    echoSimple_t echoSimple;
    reverbPlane_t reverbPlane;
    reverbLowPass_t reverbLowPass;
    reverbConvolution_t reverbConvolution;
    reverbComplete_t reverbComplete;
    robotization_t robotization;
    headPhones3D_t headPhones3D;
    vibrato_t vibrato;
    flanger_t flanger;
    reverbAllPass_t reverbAllPass;

    void (*p2callback) (const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);

}audioEffectsParameters_t;

#endif //EFFECTSTRUCTS_H