//userInterface.h 
//This file allows the programmer to communicate with the user
//Through the elements of this file, the user could define which type
//of audioEffect want to implement.

#ifndef USERINTERFACE_H
#define USERINTERFACE_H

#include "effectStructs.h"


#define UI_ERROR -1
#define UI_NOERROR 1
#define UI_CHANGE 0

#define INCVAR1 'd'
#define DECVAR1 'a'
#define INCVAR2 'c'
#define DECVAR2 'z'

#define QUIT 'q'

/////
typedef struct{
    EFFECT_TYPE effect;
    int errorUserInterface;
    
    int var1;
    int var2;
}userPreferences_t;

void userInteract(userPreferences_t * pUserPreferences);

int checkingChangeDecisions(userPreferences_t * pUserPreferences);

void tellUserFailure(char * errorMessage, int errorNumber);

#endif //USERINTERFACE_H
