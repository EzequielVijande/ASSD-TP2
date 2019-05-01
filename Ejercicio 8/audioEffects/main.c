//main.c
//main program
//This program allows the user to choose an audio effect and then apply that effect to the audio input

#include "userInterface.h"
#include "audioSupport.h"

int main()
{
    userPreferences_t userChoice;
    audioSupportResults_t audioResult;
    userInteract(&userChoice);
    if(userChoice.errorUserInterface == UI_NOERROR)
    {
        audioResult = implementAudioEffects(userChoice.effect, &(userChoice.audioEffectParameters));
        if (audioResult.succeded)
        {
            tellUserSucces();
            audioResult = uninstallAudioEffects(audioResult.pDataSupport);
        }
        if(!audioResult.succeded){
            tellUserFailure(audioResult.errorMessage, audioResult.errorNumber);
        }
    }
    return 0;
}