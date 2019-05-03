//effects.c
//backend

#include "effects.h"
#include "allPassReverb.h"
#include "echoSimple.h"
#include "planeReverb.h"
#include "lowPassReverb.h"
#include "completeReverb.h"
#include "convolutionReverb.h"
#include "robotization.h"
#include "head3D.h"
#include "vibrato.h"
#include "flanger.h"

void noneEffectCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);

void selectCallback(audioEffectsParameters_t * p2userData, int effect){
    switch(effect){
            case 1: p2userData->p2callback = echoSimpleCall; 
                    p2userData->p2effect = prepareEchoSimple();
                    p2userData->p2refresh = refreshEchoSimple;
                    break;
            case 2: p2userData->p2callback = planeReverbCall;
                    p2userData->p2effect = preparePlaneReverb();
                    p2userData->p2refresh = refreshPlaneReverb;
                    break;
            case 3: p2userData->p2callback = lowPassReverbCall;
                    p2userData->p2effect = prepareLowPassReverb();
                    p2userData->p2refresh = refreshLowPassReverb;
                    break;
            case 4: p2userData->p2callback = convolutionReverbCall;
                    p2userData->p2effect = prepareConvolutionReverb();
                    p2userData->p2refresh = refreshConvolutionReverb;
                    break;
            case 5: p2userData->p2callback = completeReverbCall;
                    p2userData->p2effect = prepareCompleteReverb();
                    p2userData->p2refresh = refreshCompleteReverb;
                    break;
            case 6: p2userData->p2callback = robotizationCall;
                    p2userData->p2effect = prepareRobotization();
                    p2userData->p2refresh = refreshRobotization;
                    break;
            case 7: p2userData->p2callback = headPhones3DCall;
                    p2userData->p2effect = prepareHeadPhones3D();
                    p2userData->p2refresh = refreshHeadPhones3D;
                    break;
            case 8: p2userData->p2callback = vibratoCall;
                    p2userData->p2effect = prepareVibrato();
                    p2userData->p2refresh = refreshVibrato;
                    break;
            case 9: p2userData->p2callback = flangerCall;
                    p2userData->p2effect = prepareFlanger();
                    p2userData->p2refresh = refreshFlanger;
                    break;
            case 0: p2userData->p2callback = allPassReverbCall;
                    p2userData->p2effect = prepareAllPassReverb();
                    p2userData->p2refresh = refreshAllPassReverb;
                    break;
            default:
                    p2userData->p2callback = noneEffectCall;
                    break;
        }
}




    


void noneEffectCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){

}



/*void convolve(float * x1, float * x2, float * xo, int N){
    int i, j;
    for(i = 0; i < N; i++){
        for(j = 0; j < i; j++){
            xo[i] += x1[j]*x2[i-j]; 
        }
    }
}*/



//"CONSTRUCTORES"






