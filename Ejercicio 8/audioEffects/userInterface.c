//userInterface.c
//frontend

#include "userInterface.h"
#include "presets.h"
#include "stdio.h"

#define ENTER '\n' //Carriage return ASCII

void echoRoutine(echoSimple_t * pData);
void planeReverbRoutine(reverbPlane_t * pData);
void lowPassReverbRoutine(reverbLowPass_t * pData);
void convolutionReverbRoutine(reverbConvolution_t * pData);
void completeReverbRoutine(reverbComplete_t* pData);
void robotizationRoutine(robotization_t * pData);
void headPhones3DRoutine(headPhones3D_t * pData);
void vibratoRoutine(vibrato_t * pData);
void flangerRoutine(flanger_t * pData);
void allPassReverbRoutine(reverbAllPass_t * pData);
void noneEffectRoutine(void);

void userInteract(userPreferences_t * pUserPreferences){
    pUserPreferences->errorUserInterface = UI_NOERROR;
    printf("Welcome to Audio Effects Interface\n\n");
    printf("10 effects will be shown then, choose the one you want to apply:\n\n");
    printf("(0) All Pass Reverb\n(1) Echo Simple\n(2) Plane Reverb\n(3) Low Pass Reverb\n"
            "(4) Complete Reverb\n(5) Convolution Reverb\n(6) Robotization\n"
            "(7) Headphones 3D\n(8) Vibrato\n(9) Flanger\n");
    char c = 'A';
    char enter = 'A';
    //while(getchar()!='\n');
    do{ 
        printf("Please, only enter the NUMBER (0 to 9) and then press ENTER, thank you\n");
        printf("(Press only q (lower case) and then ENTER to quit)\n");
        c = getchar();
        if (c != ENTER){  //si se ingreso algun caracter
            enter = getchar();
            if (enter != ENTER){ //si se ingreso mas de un caracter
                while(getchar()!='\n'); //vacio el buffer
            }
        }
    }while((enter != ENTER) || !((('0'<=c) && (c <='9')) || (c =='q'))) ;
    if(c == 'q'){
        pUserPreferences->errorUserInterface = UI_ERROR;

    }
    else
    {
        switch(c){
            case '1': echoRoutine(&(pUserPreferences->audioEffectParameters.echoSimple));
                    break;
            case '2': planeReverbRoutine(&(pUserPreferences->audioEffectParameters.reverbPlane));
                    break;
            case '3': lowPassReverbRoutine(&(pUserPreferences->audioEffectParameters.reverbLowPass));
                    break;
            case '4': convolutionReverbRoutine(&(pUserPreferences->audioEffectParameters.reverbConvolution));
                    break;
            case '5': completeReverbRoutine(&(pUserPreferences->audioEffectParameters.reverbComplete));
                    break;
            case '6': robotizationRoutine(&(pUserPreferences->audioEffectParameters.robotization));
                    break;
            case '7': headPhones3DRoutine(&(pUserPreferences->audioEffectParameters.headPhones3D));
                    break;
            case '8': vibratoRoutine(&(pUserPreferences->audioEffectParameters.vibrato));
                    break;
            case '9': flangerRoutine(&(pUserPreferences->audioEffectParameters.flanger));
                    break;
            case '0': allPassReverbRoutine(&(pUserPreferences->audioEffectParameters.reverbAllPass));
                    break;
            default:
                    noneEffectRoutine();
                    break;
        }
        pUserPreferences->effect = c - '0';
    }

    
}

void tellUserSucces(void){
    printf("In this moment is being applied the effect that you choosed\n"
            "If you want to quit, press only q\n");
    char c = '0';
    do{
        c = getchar();
    }while(c != 'q');

}

void tellUserFailure(char * errorMessage, int errorNumber){
    printf("%s\n", errorMessage);
    printf("Error number:%d\n"
            "press ANY KEY to quit and then ENTER (or just press ENTER)\n", errorNumber);
    getchar();
}


void echoRoutine(echoSimple_t * pData){
    printf("You have choosen Echo Simple!\n");
    pData->n = 0;

}
void planeReverbRoutine(reverbPlane_t * pData){
    printf("You have choosen Plane Reverberator!\n");
    pData->n = 0;

}
void lowPassReverbRoutine(reverbLowPass_t * pData){
    printf("You have choosen Low Pass Reverberator!\n");
}
void convolutionReverbRoutine(reverbConvolution_t * pData){
    printf("You have choosen Reverberetaion through Convolution!\n");
}
void completeReverbRoutine(reverbComplete_t * pData){
    printf("You have choosen Complete Reverberation!\n");
}
void robotizationRoutine(robotization_t * pData){
    printf("You have choosen Robotization!\n");
}
void headPhones3DRoutine(headPhones3D_t * pData){
    printf("You have choosen 3D effect with Headphones!\n");
}
void vibratoRoutine(vibrato_t * pData){
    printf("You have choosen Vibrato!\n");
    pData->n = 0;

}
void flangerRoutine(flanger_t * pData){
    printf("You have choosen Flanger!\n");
    pData->n = 0;
}
void noneEffectRoutine(void){

}

void allPassReverbRoutine(reverbAllPass_t * pData){
    printf("You have choosen All Pass Reverb!\n");
    pData->n = 0;
}