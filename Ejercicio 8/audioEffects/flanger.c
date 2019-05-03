//flanger.c

#include "flanger.h"
#include "math.h"
#include "stdlib.h"

#define L 8000
#define FPB 64
#define G 0.7

typedef int EFFECT_TYPE;



typedef struct{
    float freq;
    int n;
    int delayO;
    int delayE;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
}flanger_t;



void * prepareFlanger(void){
    flanger_t * p;
    p = malloc(sizeof(flanger_t));
    p->n = 0;
    p->freq = 1;
    p->delayO = L/6;
    p->delayE = L/6;
    return (void *) p;
}


void flangerCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    flanger_t * uData = (flanger_t *) userData;
    int n = (uData->n);
    float * memDerIn = uData->memoryInputsDer;
    float * memIzqIn = uData->memoryInputsIzq;
    float auxDerIn[FPB];
    float auxIzqIn[FPB];
    //float * memDerOut = (uData->vibrato).memoryOutputsDer;
    //float * memIzqOut = (uData->vibrato).memoryOutputsIzq;
    //float auxDerOut[FPB];
    //float auxIzqOut[FPB];
    int i, j, m;
    int osc = uData->delayO;
    int est = uData->delayE;
    int f = uData->freq;
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
            m =est+(osc/2)+((osc/2)*sin(((float)2)*M_PI*((float)f)*((float)i/((float)sampleRate)))); //RETARDO QUE VA ENTRE B+M y B-M
            if( (m > i) && (m < (L-1+i)) ) {

                out[2*i] = (G*memDerIn[L-1+i-m] + in[2*i])*(1/(1+G));
                out[(2*i)+1] = (G*memIzqIn[L-1+i-m] + in[(2*i)+1])*(1/(1+G));
            }
            else if (m < i){
                
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[L-1+i-m];

            }
            else{
                
                //PROBLEMAS CON EL LARGO DEL ARREGLO DE MEMORIA AUXILIAR (L) O LARGO DE RETARDO.
            }
            //aqui se llenan los buffers auxiliares para luego actualizar la memoria.
            auxDerIn[i] = in[2*i];
            auxIzqIn[i] = in[(2*i)+1];
            //auxDerOut[i] = out[2*i];
            //auxIzqOut[i] = out[(2*i)+1];
        
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
    uData->n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}

void refreshFlanger(int var1, int var2, void * p2effect){
    flanger_t * pData = (flanger_t *) p2effect;
    pData->delayO = L/((12-var1)*3);
    pData->delayE = L/((12-var2)*3);
}
