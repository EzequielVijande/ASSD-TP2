//audioSupport.h
//This file manage the audioResource and implement the effects.
//backend

#ifndef AUDIOSUPPORT_H
#define AUDIOSUPPORT_H


#include "stdbool.h"

typedef struct{
    bool succeded;
    char * errorMessage; 
    int errorNumber;
    void * pDataSupport;


}audioSupportResults_t;

audioSupportResults_t implementAudioEffects(int effect, void * pEffectsParam);
audioSupportResults_t uninstallAudioEffects(void * pDataSupport);

#endif //AUDIOSUPPORT_H