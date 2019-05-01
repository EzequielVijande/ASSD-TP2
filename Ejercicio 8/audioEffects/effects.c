//effects.c
//backend

#include "effects.h"
#include "effectStructs.h"
#include "stdio.h"
#include "math.h"

#define L 20000
#define M 400
#define F 7
#define B 200//
#define E 5800
#define G 0.7
#define FPB 64
#define MI 19800//retardo constante de la entrada
#define MO 5800 //retardo constante de la salida

void echoSimpleCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void planeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void lowPassReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void convolutionReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void completeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void robotizationCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void headPhones3DCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void vibratoCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void flangerCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void noneEffectCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);
void allPassReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);


void selectCallback(void * p, int effect){
    audioEffectsParameters_t * p2userData = (audioEffectsParameters_t *) p; //Casteo de puntero.
    switch(effect){
            case 1: p2userData->p2callback = echoSimpleCall;
                    //prepareEchoSimple(p2userData);
                    break;
            case 2: p2userData->p2callback = planeReverbCall;
                    //preparePlaneReverb(p2userData);
                    break;
            case 3: p2userData->p2callback = lowPassReverbCall;
                    //prepareLowPassReverb(p2userData);
                    break;
            case 4: p2userData->p2callback = convolutionReverbCall;
                    //prepareConvolutionReverb(p2userData);
                    break;
            case 5: p2userData->p2callback = completeReverbCall;
                    //prepareCompleteReverb(p2userData);
                    break;
            case 6: p2userData->p2callback = robotizationCall;
                    break;
            case 7: p2userData->p2callback = headPhones3DCall;
                    break;
            case 8: p2userData->p2callback = vibratoCall;
                    break;
            case 9: p2userData->p2callback = flangerCall;
                    break;
            case 0: p2userData->p2callback = allPassReverbCall;
                    break;
            default:
                    p2userData->p2callback = noneEffectCall;
                    break;
        }
}

void echoSimpleCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    audioEffectsParameters_t * uData = (audioEffectsParameters_t *) userData;
    int n = ((uData->echoSimple).n);
    float * memDerIn = (uData->echoSimple).memoryInputsDer;
    float * memIzqIn = (uData->echoSimple).memoryInputsIzq;
    float auxDerIn[FPB];
    float auxIzqIn[FPB];
    //float * memDerOut = (uData->vibrato).memoryOutputsDer;
    //float * memIzqOut = (uData->vibrato).memoryOutputsIzq;
    //float auxDerOut[FPB];
    //float auxIzqOut[FPB];
    int i, j, m;
    m = MI;
    for(i=0; i < framesPerBuffer; i++)
    {   
        if(n < (L-1)){//inicio llenando la memoria con "L" datos (tanto para Izq como para Der).
            memDerIn[n] = in[2*i]; //lleno la memoria de los pares (audio derecho).
            memIzqIn[n] = in[(2*i)+1]; //idem audio izquierda (impares).
            //memIzqOut[n] = 0.0;
            //memDerOut[n] = 0.0;
            out[2*i] = 0.0;
            out[(2*i)+1] = 0.0;
            n++;
        }
        else{ //si la memoria se lleno por primera vez, procedo a realizar el efecto
            if( (m > i) && (m < (L-1+i)) ) {
                out[2*i] = (G*memDerIn[L-1+i-m] + in[2*i])*(1/(1+G));
                out[(2*i)+1] = (G*memIzqIn[L-1+i-m] + in[(2*i)+1])*(1/(1+G));
            }
            else if (m < i){
                printf("retardo chico\n");
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[L-1+i-m];

            }
            else{
                printf("problemas de reatardo\n");
                //PROBLEMAS CON EL LARGO DEL ARREGLO DE MEMORIA AUXILIAR (L) O LARGO DE RETARDO.
            }
            //aqui se llenan los buffers auxiliares para luego actualizar la memoria.
            auxDerIn[i] = in[2*i];
            auxIzqIn[i] = in[(2*i)+1];
            //auxDerOut[i] = out[2*i];
            //auxIzqOut[i] = out[(2*i)+1];
        
        }

        if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
            printf("parametro de fue de rango\n");
            out[2*i] = 0;
            out[(2*i)+1] = 0;
        }
        
    }
    //aqui se procede a actualizar la memoria, siempre y cuando esta ya se haya llenado en un principio
    if(!(n < (L-1)))
    {
        for(j = 0; j < L; j++){
        if (j < L-FPB){
            memDerIn[j] = memDerIn[j+FPB];
            memIzqIn[j] = memIzqIn[j+FPB];
            //memDerOut[j] = memDerOut[j+FPB];
            //memIzqOut[j] = memIzqOut[j+FPB];
        }
        else{
            memDerIn[j] = auxDerIn[j - L + FPB];
            memIzqIn[j] = auxIzqIn[j - L + FPB];
            //memDerOut[j] = auxDerOut[j - L + FPB];
            //memIzqOut[j] = auxIzqOut[j - L + FPB];
        }
    }
        
    }
    (uData->echoSimple).n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}

void planeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    audioEffectsParameters_t * uData = (audioEffectsParameters_t *) userData;
    int n = ((uData->reverbPlane).n);
    //float * memDerIn = (uData->reverbPlane).memoryInputsDer;
    //float * memIzqIn = (uData->reverbPlane).memoryInputsIzq;
    //float auxDerIn[FPB];
    //float auxIzqIn[FPB];
    float * memDerOut = (uData->reverbPlane).memoryOutputsDer;
    float * memIzqOut = (uData->reverbPlane).memoryOutputsIzq;
    float auxDerOut[FPB];
    float auxIzqOut[FPB];
    int i, j, m;
    m = MI; //retardo constante de la entrada.
    for(i=0; i < framesPerBuffer; i++)
    {   
        if(n < (L-1)){//inicio llenando la memoria con "L" datos (tanto para Izq como para Der).
            //memDerIn[n] = in[2*i]; //lleno la memoria de los pares (audio derecho).
            //memIzqIn[n] = in[(2*i)+1]; //idem audio izquierda (impares).
            memIzqOut[n] = 0.0;
            memDerOut[n] = 0.0;
            out[2*i] = 0.0;
            out[(2*i)+1] = 0.0;
            n++;
        }
        else{ //si la memoria se lleno por primera vez, procedo a realizar el efecto
            if( (m > i) && (m < (L-1+i)) ) {
                out[2*i] =  ((G * memDerOut[L-1+i-m]) + in[2*i])*(1-G);
                out[(2*i)+1] = ((G * memIzqOut[L-1+i-m]) + in[(2*i)+1])*(1-G);
            }
            else if (m < i){
                printf("retardo chico\n");
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[i-m];

            }
            else{
                printf("problemas de reatardo\n");
                //PROBLEMAS CON EL LARGO DEL ARREGLO DE MEMORIA AUXILIAR (L) O LARGO DE RETARDO.
            }
            //aqui se llenan los buffers auxiliares para luego actualizar la memoria.
            //auxDerIn[i] = in[2*i];
            //auxIzqIn[i] = in[(2*i)+1];
            auxDerOut[i] = out[2*i];
            auxIzqOut[i] = out[(2*i)+1];
        
        }

        if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
            out[2*i] = 0;
            out[(2*i)+1] = 0;
        }
        
    }
    //aqui se procede a actualizar la memoria, siempre y cuando esta ya se haya llenado en un principio
    if(!(n < (L-1)))
    {
        for(j = 0; j < L; j++){
        if (j < L-FPB){
            //memDerIn[j] = memDerIn[j+FPB];
            //memIzqIn[j] = memIzqIn[j+FPB];
            memDerOut[j] = memDerOut[j+FPB];
            memIzqOut[j] = memIzqOut[j+FPB];
        }
        else{
            //memDerIn[j] = auxDerIn[j - L + FPB];
            //memIzqIn[j] = auxIzqIn[j - L + FPB];
            memDerOut[j] = auxDerOut[j - L + FPB];
            memIzqOut[j] = auxIzqOut[j - L + FPB];
        }
    }
        
    }
    (uData->reverbPlane).n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}

void lowPassReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    audioEffectsParameters_t * uData = (audioEffectsParameters_t *) userData;
    int n = ((uData->reverbPlane).n);
    float * memDerIn = (uData->reverbPlane).memoryInputsDer;
    float * memIzqIn = (uData->reverbPlane).memoryInputsIzq;
    float auxDerIn[FPB];
    float auxIzqIn[FPB];
    float * memDerOut = (uData->reverbPlane).memoryOutputsDer;
    float * memIzqOut = (uData->reverbPlane).memoryOutputsIzq;
    float auxDerOut[FPB];
    float auxIzqOut[FPB];
    int i, j, m;
    m = MI; //retardo constante de la entrada.
    for(i=0; i < framesPerBuffer; i++)
    {   
        if(n < (L-1)){//inicio llenando la memoria con "L" datos (tanto para Izq como para Der).
            memDerIn[n] = in[2*i]; //lleno la memoria de los pares (audio derecho).
            memIzqIn[n] = in[(2*i)+1]; //idem audio izquierda (impares).
            memIzqOut[n] = 0.0;
            memDerOut[n] = 0.0;
            out[2*i] = 0.0;
            out[(2*i)+1] = 0.0;
            n++;
        }
        else{ //si la memoria se lleno por primera vez, procedo a realizar el efecto
            if( (m > i) && (m < (L-1+i)) ) {
                out[2*i] = memDerIn[L-1+i-m] + (G * memDerOut[L-1+i-m]) - (G * in[2*i]);
                out[(2*i)+1] = memIzqIn[L-1+i-m] + (G * memIzqOut[L-1+i-m]) - (G * in[(2*i)+1]);
            }
            else if (m < i){
                printf("retardo chico\n");
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[L-1+i-m];

            }
            else{
                printf("problemas de reatardo\n");
                //PROBLEMAS CON EL LARGO DEL ARREGLO DE MEMORIA AUXILIAR (L) O LARGO DE RETARDO.
            }
            //aqui se llenan los buffers auxiliares para luego actualizar la memoria.
            auxDerIn[i] = in[2*i];
            auxIzqIn[i] = in[(2*i)+1];
            auxDerOut[i] = out[2*i];
            auxIzqOut[i] = out[(2*i)+1];
        
        }

        if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
            out[2*i] = 0;
            out[(2*i)+1] = 0;
        }
        
    }
    //aqui se procede a actualizar la memoria, siempre y cuando esta ya se haya llenado en un principio
    if(!(n < (L-1)))
    {
        for(j = 0; j < L; j++){
            if (j < L-FPB){
                memDerIn[j] = memDerIn[j+FPB];
                memIzqIn[j] = memIzqIn[j+FPB];
                memDerOut[j] = memDerOut[j+FPB];
                memIzqOut[j] = memIzqOut[j+FPB];
            }
            else{
                memDerIn[j] = auxDerIn[j - L + FPB];
                memIzqIn[j] = auxIzqIn[j - L + FPB];
                memDerOut[j] = auxDerOut[j - L + FPB];
                memIzqOut[j] = auxIzqOut[j - L + FPB];
            }
        }
        
    }
    (uData->reverbPlane).n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}

void convolutionReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    
}

void completeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    
}

void robotizationCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    
}

void headPhones3DCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    
}

void vibratoCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    audioEffectsParameters_t * uData = (audioEffectsParameters_t *) userData;
    int n = ((uData->vibrato).n);
    float * memDerIn = (uData->vibrato).memoryInputsDer;
    float * memIzqIn = (uData->vibrato).memoryInputsIzq;
    float auxDerIn[FPB];
    float auxIzqIn[FPB];
    float * memDerOut = (uData->vibrato).memoryOutputsDer;
    float * memIzqOut = (uData->vibrato).memoryOutputsIzq;
    float auxDerOut[FPB];
    float auxIzqOut[FPB];
    int i, j, m;
    
    for(i=0; i < framesPerBuffer; i++)
    {   
        if(n < (L-1)){//inicio llenando la memoria con "L" datos (tanto para Izq como para Der).
            memDerIn[n] = in[2*i]; //lleno la memoria de los pares (audio derecho).
            memIzqIn[n] = in[(2*i)+1]; //idem audio izquierda (impares).
            memIzqOut[n] = 0.0;
            memDerOut[n] = 0.0;
            out[2*i] = 0.0;
            out[(2*i)+1] = 0.0;
            n++;
        }
        else{ //si la memoria se lleno por primera vez, procedo a realizar el efecto
            m =B+(M/2)+((M/2)*sin(((float)2)*M_PI*((float)F)*((float)i/((float)sampleRate)))); //RETARDO QUE VA ENTRE B+M y B-M
            if( (m > i) && (m < (L-1+i)) ) {
                out[2*i] = memDerIn[L-1+i-m];
                out[(2*i)+1] = memIzqIn[L-1+i-m];
            }
            else if (m < i){
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[L-1+i-m];

            }
            else{
                printf("problemas de reatardo\n");
                //PROBLEMAS CON EL LARGO DEL ARREGLO DE MEMORIA AUXILIAR (L) O LARGO DE RETARDO.
            }
            //aqui se llenan los buffers auxiliares para luego actualizar la memoria.
            auxDerIn[i] = in[2*i];
            auxIzqIn[i] = in[(2*i)+1];
            auxDerOut[i] = out[2*i];
            auxIzqOut[i] = out[(2*i)+1];
        
        }

        if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
            out[2*i] = 0;
            out[(2*i)+1] = 0;
        }
        
    }
    //aqui se procede a actualizar la memoria, siempre y cuando esta ya se haya llenado en un principio
    if(!(n < (L-1)))
    {
        for(j = 0; j < L; j++){
        if (j < L-FPB){
            memDerIn[j] = memDerIn[j+FPB];
            memIzqIn[j] = memIzqIn[j+FPB];
            memDerOut[j] = memDerOut[j+FPB];
            memIzqOut[j] = memIzqOut[j+FPB];
        }
        else{
            memDerIn[j] = auxDerIn[j - L + FPB];
            memIzqIn[j] = auxIzqIn[j - L + FPB];
            memDerOut[j] = auxDerOut[j - L + FPB];
            memIzqOut[j] = auxIzqOut[j - L + FPB];
        }
    }
        
    }
    (uData->vibrato).n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}
    

void flangerCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    audioEffectsParameters_t * uData = (audioEffectsParameters_t *) userData;
    int n = ((uData->flanger).n);
    float * memDerIn = (uData->flanger).memoryInputsDer;
    float * memIzqIn = (uData->flanger).memoryInputsIzq;
    float auxDerIn[FPB];
    float auxIzqIn[FPB];
    //float * memDerOut = (uData->vibrato).memoryOutputsDer;
    //float * memIzqOut = (uData->vibrato).memoryOutputsIzq;
    //float auxDerOut[FPB];
    //float auxIzqOut[FPB];
    int i, j, m;
    for(i=0; i < framesPerBuffer; i++)
    {   
        if(n < (L-1)){//inicio llenando la memoria con "L" datos (tanto para Izq como para Der).
            memDerIn[n] = in[2*i]; //lleno la memoria de los pares (audio derecho).
            memIzqIn[n] = in[(2*i)+1]; //idem audio izquierda (impares).
            //memIzqOut[n] = 0.0;
            //memDerOut[n] = 0.0;
            out[2*i] = 0.0;
            out[(2*i)+1] = 0.0;
            n++;
        }
        else{ //si la memoria se lleno por primera vez, procedo a realizar el efecto
            m =B+(M/2)+((M/2)*sin(((float)2)*M_PI*((float)F)*((float)i/((float)sampleRate)))); //RETARDO QUE VA ENTRE B+M y B-M
            if( (m > i) && (m < (L-1+i)) ) {

                out[2*i] = (G*memDerIn[L-1+i-m] + in[2*i])*(1/(1+G));
                out[(2*i)+1] = (G*memIzqIn[L-1+i-m] + in[(2*i)+1])*(1/(1+G));
            }
            else if (m < i){
                printf("retardo chico\n");
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[L-1+i-m];

            }
            else{
                printf("problemas de reatardo\n");
                //PROBLEMAS CON EL LARGO DEL ARREGLO DE MEMORIA AUXILIAR (L) O LARGO DE RETARDO.
            }
            //aqui se llenan los buffers auxiliares para luego actualizar la memoria.
            auxDerIn[i] = in[2*i];
            auxIzqIn[i] = in[(2*i)+1];
            //auxDerOut[i] = out[2*i];
            //auxIzqOut[i] = out[(2*i)+1];
        
        }

        if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
            printf("parametro de fue de rango\n");
            out[2*i] = 0;
            out[(2*i)+1] = 0;
        }
        
    }
    //aqui se procede a actualizar la memoria, siempre y cuando esta ya se haya llenado en un principio
    if(!(n < (L-1)))
    {
        for(j = 0; j < L; j++){
        if (j < L-FPB){
            memDerIn[j] = memDerIn[j+FPB];
            memIzqIn[j] = memIzqIn[j+FPB];
            //memDerOut[j] = memDerOut[j+FPB];
            //memIzqOut[j] = memIzqOut[j+FPB];
        }
        else{
            memDerIn[j] = auxDerIn[j - L + FPB];
            memIzqIn[j] = auxIzqIn[j - L + FPB];
            //memDerOut[j] = auxDerOut[j - L + FPB];
            //memIzqOut[j] = auxIzqOut[j - L + FPB];
        }
    }
        
    }
    (uData->flanger).n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}

void noneEffectCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){

}

void allPassReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    audioEffectsParameters_t * uData = (audioEffectsParameters_t *) userData;
    int n = ((uData->reverbAllPass).n);
    float * memDerIn = (uData->reverbAllPass).memoryInputsDer;
    float * memIzqIn = (uData->reverbAllPass).memoryInputsIzq;
    float auxDerIn[FPB];
    float auxIzqIn[FPB];
    float * memDerOut = (uData->reverbAllPass).memoryOutputsDer;
    float * memIzqOut = (uData->reverbAllPass).memoryOutputsIzq;
    float auxDerOut[FPB];
    float auxIzqOut[FPB];
    int i, j, m;
    m = MI; //retardo constante de la entrada.
    for(i=0; i < framesPerBuffer; i++)
    {   
        if(n < (L-1)){//inicio llenando la memoria con "L" datos (tanto para Izq como para Der).
            memDerIn[n] = in[2*i]; //lleno la memoria de los pares (audio derecho).
            memIzqIn[n] = in[(2*i)+1]; //idem audio izquierda (impares).
            memIzqOut[n] = 0.0;
            memDerOut[n] = 0.0;
            out[2*i] = 0.0;
            out[(2*i)+1] = 0.0;
            n++;
        }
        else{ //si la memoria se lleno por primera vez, procedo a realizar el efecto
            if( (m > i) && (m < (L-1+i)) ) {
                out[2*i] = memDerIn[L-1+i-m] + (G * memDerOut[L-1+i-m]) - (G * in[2*i]);
                out[(2*i)+1] = memIzqIn[L-1+i-m] + (G * memIzqOut[L-1+i-m]) - (G * in[(2*i)+1]);
            }
            else if (m < i){
                printf("retardo chico\n");
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[L-1+i-m];

            }
            else{
                printf("problemas de reatardo\n");
                //PROBLEMAS CON EL LARGO DEL ARREGLO DE MEMORIA AUXILIAR (L) O LARGO DE RETARDO.
            }
            //aqui se llenan los buffers auxiliares para luego actualizar la memoria.
            auxDerIn[i] = in[2*i];
            auxIzqIn[i] = in[(2*i)+1];
            auxDerOut[i] = out[2*i];
            auxIzqOut[i] = out[(2*i)+1];
        
        }

        if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
            out[2*i] = 0;
            out[(2*i)+1] = 0;
        }
        
    }
    //aqui se procede a actualizar la memoria, siempre y cuando esta ya se haya llenado en un principio
    if(!(n < (L-1)))
    {
        for(j = 0; j < L; j++){
            if (j < L-FPB){
                memDerIn[j] = memDerIn[j+FPB];
                memIzqIn[j] = memIzqIn[j+FPB];
                memDerOut[j] = memDerOut[j+FPB];
                memIzqOut[j] = memIzqOut[j+FPB];
            }
            else{
                memDerIn[j] = auxDerIn[j - L + FPB];
                memIzqIn[j] = auxIzqIn[j - L + FPB];
                memDerOut[j] = auxDerOut[j - L + FPB];
                memIzqOut[j] = auxIzqOut[j - L + FPB];
            }
        }
        
    }
    (uData->reverbAllPass).n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}
