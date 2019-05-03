//audioSupport.h
//This file manage the audioResource and implement the effects.
//backend

#ifndef AUDIOSUPPORT_H
#define AUDIOSUPPORT_H


#include "stdbool.h"
#include "effectStructs.h"

typedef struct{
    bool succeded;
    char * errorMessage; 
    int errorNumber;
    void * pDataSupport;


}audioSupportResults_t;


void refreshParamsEfects(int var1, int var2, int effect);
audioSupportResults_t implementAudioEffects(int effect, audioEffectsParameters_t * pEffectsParam);
audioSupportResults_t uninstallAudioEffects(void * pDataSupport, audioEffectsParameters_t * p);

#endif //AUDIOSUPPORT_H