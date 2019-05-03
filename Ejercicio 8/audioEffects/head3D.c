//head3D.c

#include "head3D.h"
#include "math.h"
#include "stdlib.h"

#define L 8000
#define FPB 64

typedef int EFFECT_TYPE;
typedef float SAMPLE;


typedef struct{
    float teta;           //comentar que representan estos parámetros
    float wo;
    float fs;
    float memDerIn[L];
    float memIzqIn[L];
    float memDerOut;
    float memIzqOut;

}headPhones3D_t;

void * prepareHeadPhones3D(void){
    headPhones3D_t * p;
    p = malloc(sizeof(headPhones3D_t));
    return (void *) p;
}

void headPhones3DCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    headPhones3D_t * pData = (headPhones3D_t *) userData;
    float tetaRads = pData->teta * M_PI / 180;
    float alpha = 1.05+0.95*cos(tetaRads*180/150);
    float a = (pData->wo) + alpha * (pData->fs);
    float b = (pData->wo) + (pData->fs);
    float c = (pData->wo) - alpha * pData->fs;
    float d = pData->wo - pData->fs;
    float tao;
    float auxDerIn[FPB];
    float auxIzqIn[FPB];
    if((pData->teta >= -90) && (pData->teta <= 90)){
        tao = (-1*a/c)*cos(tetaRads);
    }
    else{
        tao = (a/c)*(fabs(tetaRads)-(M_PI/2));
    }
    int taoInt = (int) tao;
    int i;
    for(i = 0; i < framesPerBuffer; i++){
        if(i == 0){
            out[2*i] = -1*d*pData->memDerOut + a*pData->memDerIn[L-1-taoInt] + c*pData->memDerIn[L-1-taoInt-1];
            out[(2*i)+1] = -1*d*pData->memIzqOut + a*pData->memIzqIn[L-1-taoInt] + c*pData->memIzqIn[L-1-taoInt-1];
        }
        else if(taoInt >= i){
            out[2*i] = (-1*d*out[2*(i-1)] + a*pData->memDerIn[L-1-taoInt] + c*pData->memDerIn[L-1-taoInt-1])/b;
            out[(2*i)+1] = (-1*d*out[(2*(i-1))+1] + a*pData->memIzqIn[L-1-taoInt] + c*pData->memIzqIn[L-1-taoInt-1])/b;
        }
        else if(taoInt < i){
            out[2*i] = (-1*d*in[2*(i-1)] + a*in[2*(i-taoInt)] + c*in[2*(i-taoInt-1)])/b;
            out[(2*i)+1] = (-1*d*out[(2*(i-1))+1] + a*in[(2*(i-taoInt))+1] + c*in[2*(i-taoInt-1)+1])/b;
        }
        auxDerIn[i] = in[2*i];
        auxIzqIn[i] = in[(2*i)+1];
    }
    pData->memDerOut = out[2*(i-1)];
    pData->memIzqOut = out[2*(i-1)+1];
    int j;
    for(j = 0; j < L; j++){
        if (j < L-FPB){
            pData->memDerIn[j] = pData->memDerIn[j+FPB];
            pData->memIzqIn[j] = pData->memIzqIn[j+FPB];
        }
        else{
            pData->memDerIn[j] = auxDerIn[j - L + FPB];
            pData->memIzqIn[j] = auxIzqIn[j - L + FPB];
        }
    }
    (pData->teta)++;
    if(pData->teta == 180){
        pData->teta = 0;
    }
}

void refreshHeadPhones3D(int var1, int var2, void * p2effect){
    
}