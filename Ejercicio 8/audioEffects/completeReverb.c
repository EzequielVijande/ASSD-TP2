//completeReverb.c
#include "completeReverb.h"
#include "math.h"
#include "stdlib.h"
#include "allPassReverb.h"
#include "planeReverb.h"
#include "echoSimple.h"

#define L 20000
#define FPB 64

typedef struct{
    int delay;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
    int n;
}echoSimple_t;


typedef struct{
    int delay;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
    float memoryOutputsDer[L];
    float memoryOutputsIzq[L];
    int n;
}reverbAllPass_t;


typedef struct{
    reverbAllPass_t * pAll;
    echoSimple_t * pPlane;
    reverbAllPass_t  allPassData;
    echoSimple_t  echoData;
    void (*p2echoSimple)(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
    void (*p2allPassReverb)(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate); 
}reverbComplete_t;



void * prepareCompleteReverb(void){
    reverbComplete_t * p;
    p = malloc(sizeof(reverbComplete_t));
    p->allPassData.delay = L/2;
    p->allPassData.n = 0;
    p->echoData.delay = L/2;
    p->echoData.n = 0;
    p->pAll = &(p->allPassData);
    p->pPlane = &(p->echoData);
    p->p2echoSimple = echoSimpleCall;
    p->p2allPassReverb = allPassReverbCall;
    return (void *) p;
}


void completeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    reverbComplete_t * uData = (reverbComplete_t *) userData;
    

    float W[2*FPB];
    float Z[2*FPB];
    
    uData->p2allPassReverb(in, W, framesPerBuffer, (void * ) uData->pAll, sampleRate);
    uData->p2echoSimple(W, Z, framesPerBuffer, (void * ) uData->pPlane, sampleRate);
    int i;
    for(i = 0; i < framesPerBuffer; i++){
        out[2*i] = (Z[2*i] + W[2*i])/2.0;
        out[(2*i)+1] = (Z[(2*i)+1] + W[(2*i)+1])/2.0;
    }
    
}


void refreshCompleteReverb(int var1, int var2, void * p2effect){
    
}