//planeReverb.c

#include "planeReverb.h"
#include "math.h"
#include "stdlib.h"

#define L 20000
#define FPB 64
#define G 0.7




typedef struct{
    int delay;
    float memoryInputsDer[L];
    float memoryInputsIzq[L];
    float memoryOutputsDer[L];
    float memoryOutputsIzq[L];
    int n;
}reverbPlane_t;




void * preparePlaneReverb(void){
    reverbPlane_t * p;
    p = malloc(sizeof(reverbPlane_t));
    p->n = 0;
    p->delay = L/2;
    return (void *) p;
}






void planeReverbCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    reverbPlane_t * uData = (reverbPlane_t *) userData;
    int n = (uData->n);
    //float * memDerIn = (uData->reverbPlane).memoryInputsDer;
    //float * memIzqIn = (uData->reverbPlane).memoryInputsIzq;
    //float auxDerIn[FPB];
    //float auxIzqIn[FPB];
    float * memDerOut = uData->memoryOutputsDer;
    float * memIzqOut = uData->memoryOutputsIzq;
    float auxDerOut[FPB];
    float auxIzqOut[FPB];
    int i, j, m;
    m = uData->delay; //retardo constante de la entrada.
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
                
                out[2*i] = in[i-m];
                out[(2*i)+1] = in[i-m];

            }
            else{
                
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
    uData->n = n; //esto es para registrar n cuando se esta llenando la memoria al principio
}

void refreshPlaneReverb(int var1, int var2, void * p2effect){
    reverbPlane_t * pData = (reverbPlane_t *) p2effect;
    pData->delay = L/(12-var1); 
}
