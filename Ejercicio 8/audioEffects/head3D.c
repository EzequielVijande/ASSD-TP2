//head3D.c

#include "head3D.h"
#include "math.h"
#include "stdlib.h"

#define L 8000
#define FPB 64

typedef int EFFECT_TYPE;
typedef float SAMPLE;


typedef struct{
    int a;           //comentar que representan estos parámetros
    int b;
}headPhones3D_t;

void * prepareHeadPhones3D(void){
    headPhones3D_t * p;
    p = malloc(sizeof(headPhones3D_t));
    return (void *) p;
}

void headPhones3DCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    
}

void refreshHeadPhones3D(int var1, int var2, void * p2effect){
    
}