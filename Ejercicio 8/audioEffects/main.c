//main.c
//main program
//This program allows the user to choose an audio effect and then apply that effect to the audio input

#include "userInterface.h"
#include "audioSupport.h"
#include "stdio.h"
int main(void){
    userPreferences_t userChoice;
    audioSupportResults_t audioResult;
    audioEffectsParameters_t audioParams;
    userInteract(&userChoice);
    if(userChoice.errorUserInterface == UI_NOERROR)
    {
        audioResult = implementAudioEffects(userChoice.effect, &audioParams); 
        if (audioResult.succeded)                                                   
        {                                                                          
            while(userChoice.errorUserInterface != UI_ERROR){
                userChoice.errorUserInterface = checkingChangeDecisions(&userChoice);
                if(userChoice.errorUserInterface == UI_CHANGE){
                    audioParams.p2refresh(userChoice.var1, userChoice.var2, audioParams.p2effect);
                }
            }
            audioResult = uninstallAudioEffects(audioResult.pDataSupport, &audioParams); //usuario quiso salir o hubo error en la UI
        }
        if(!audioResult.succeded){
            tellUserFailure(audioResult.errorMessage, audioResult.errorNumber);
        }
    }
    return 0;
}