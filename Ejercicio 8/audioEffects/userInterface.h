//userInterface.h 
//This file allows the programmer to communicate with the user
//Through the elements of this file, the user could define which type
//of audioEffect want to implement.

#ifndef USERINTERFACE_H
#define USERINTERFACE_H

#include "effectStructs.h"


#define UI_ERROR -1
#define UI_NOERROR 1

/////
typedef struct{
    EFFECT_TYPE effect;
    int errorUserInterface;
    audioEffectsParameters_t audioEffectParameters;
}userPreferences_t;

void userInteract(userPreferences_t * pUserPreferences);

void tellUserSucces(void);

void tellUserFailure(char * errorMessage, int errorNumber);

#endif //USERINTERFACE_H
