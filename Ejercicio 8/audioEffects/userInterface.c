//userInterface.c
//frontend

#include "userInterface.h"
#include "presets.h"
#include "stdio.h"



#define UPPER_LIMIT 10
#define DOWN_LIMIT 0

#define ENTER '\n' //Carriage return ASCII

void echoRoutine(userPreferences_t * pUserPreferences);
void planeReverbRoutine(userPreferences_t * pUserPreferences);
void lowPassReverbRoutine(userPreferences_t * pUserPreferences);
void convolutionReverbRoutine(userPreferences_t * pUserPreferences);
void completeReverbRoutine(userPreferences_t * pUserPreferences);
void robotizationRoutine(userPreferences_t * pUserPreferences);
void headPhones3DRoutine(userPreferences_t * pUserPreferences);
void vibratoRoutine(userPreferences_t * pUserPreferences);
void flangerRoutine(userPreferences_t * pUserPreferences);
void allPassReverbRoutine(userPreferences_t * pUserPreferences);
void noneEffectRoutine(void);

void incVar(int * var);
void decVar(int * var);

void userInteract(userPreferences_t * pUserPreferences){
    pUserPreferences->errorUserInterface = UI_NOERROR;
    printf("Welcome to Audio Effects Interface\n\n");
    printf("10 effects will be shown then, choose the one you want to apply:\n\n");
    printf("(0) All Pass Reverb\n(1) Echo Simple\n(2) Plane Reverb\n(3) Low Pass Reverb\n"
            "(4) Convolution Reverb\n(5) Complete Reverb\n(6) Robotization\n"
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
            case '1': echoRoutine(pUserPreferences);
                    break;
            case '2': planeReverbRoutine(pUserPreferences);
                    break;
            case '3': lowPassReverbRoutine(pUserPreferences);
                    break;
            case '4': convolutionReverbRoutine(pUserPreferences);
                    break;
            case '5': completeReverbRoutine(pUserPreferences);
                    break;
            case '6': robotizationRoutine(pUserPreferences);
                    break;
            case '7': headPhones3DRoutine(pUserPreferences);
                    break;
            case '8': vibratoRoutine(pUserPreferences);
                    break;
            case '9': flangerRoutine(pUserPreferences);
                    break;
            case '0': allPassReverbRoutine(pUserPreferences);
                    break;
            default:
                    noneEffectRoutine();
                    break;
        }
        pUserPreferences->effect = c - '0';
    }

    
}

int checkingChangeDecisions(userPreferences_t * pUserPreferences){
    printf("In this moment is being applied the effect that you choosed, Enjoy it!\n"
            "(If you want to quit, press only q and then ENTER)\n");
    int ret = UI_NOERROR;
    char c = '0';
    //do{
    c = getchar();
    //}while( (c != QUIT) && (c != INCVAR1) && (c != INCVAR2) && (c != DECVAR1) && (c != DECVAR2) );
    switch(c){
        case QUIT: ret = UI_ERROR;
                break;
        case INCVAR1: incVar(&(pUserPreferences->var1));
                    ret = UI_CHANGE;
                    break;
        case INCVAR2: incVar(&(pUserPreferences->var2));
                    ret = UI_CHANGE;
                    break;
        case DECVAR1: decVar(&(pUserPreferences->var1));
                    ret = UI_CHANGE;
                    break;
        case DECVAR2: decVar(&(pUserPreferences->var2));
                    ret = UI_CHANGE;
                    break;
        default: ret = UI_NOERROR;
                break;

    }
    return ret;

}

void tellUserFailure(char * errorMessage, int errorNumber){
    printf("%s\n", errorMessage);
    printf("Error number:%d\n"
            "press ANY KEY to quit and then ENTER (or just press ENTER)\n", errorNumber);
    getchar();
}


void echoRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Echo Simple!\n"
            "enter %c to obtain more eco delay\n"
            "enter %c to reduce delay\n", INCVAR1, DECVAR1);
    
    pUserPreferences->var1 = 5; //preset!

}
void planeReverbRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Plane Reverberator!\n"
            "enter %c to obtain more delay\n"
            "enter %c to reduce delay\n", INCVAR1, DECVAR1);
    pUserPreferences->var1 = 5; //preset!

}
void lowPassReverbRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Low Pass Reverberator!\n"
            "enter %c to obtain more delay\n"
            "enter %c to reduce delay\n", INCVAR1, DECVAR1);
    pUserPreferences->var1 = 5; //preset!
}
void convolutionReverbRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Reverberetaion through Convolution!\n");
}
void completeReverbRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Complete Reverberator!\n"
            "enter %c to obtain more delay\n"
            "enter %c to reduce delay\n"
            "enter %c to obtain more attenuation\n"
            "enter %c to reduce attenuation\n", INCVAR1, DECVAR1, DECVAR1, DECVAR2);
    pUserPreferences->var1 = 5; //preset!
    pUserPreferences->var2 = 5;
}
void robotizationRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Robotization!\n");
}
void headPhones3DRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen 3D effect with Headphones!\n");
}
void vibratoRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Vibrato!\n"
            "enter %c to obtain more delay\n"
            "enter %c to reduce delay\n"
            "enter %c to upper frecuency\n"
            "enter %c to reduce frecuency\n", INCVAR1, DECVAR1, DECVAR1, DECVAR2);
    pUserPreferences->var1 = 5; //preset!
    pUserPreferences->var2 = 5;

}
void flangerRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen Flanger!\n"
            "enter %c to obtain more oscilant delay\n"
            "enter %c to reduce oscilant delay\n"
            "enter %c to upper stacionary delay\n"
            "enter %c to reduce stacionary delay\n", INCVAR1, DECVAR1, DECVAR1, DECVAR2);
    pUserPreferences->var1 = 5; //preset!
    pUserPreferences->var2 = 5;
}

void allPassReverbRoutine(userPreferences_t * pUserPreferences){
    printf("You have choosen All Pass Reverb!\n"
            "enter %c to obtain more eco delay\n"
            "enter %c to reduce delay\n", INCVAR1, DECVAR1);

    pUserPreferences->var1 = 5; //preset!
}

void noneEffectRoutine(void){

}

void incVar(int * var){
    if((*var) < UPPER_LIMIT){
        (*var)++;
    }
}
void decVar(int * var){
    if((*var) > DOWN_LIMIT){
        (*var)--;
    }
}