//robotization.c

#include "robotization.h"
#include "math.h"
#include "stdlib.h"
#include "fftC.h"
#include "hanning.h"


#define L 8000
#define FPB 64

typedef int EFFECT_TYPE;
typedef float SAMPLE;

typedef struct{
    float memDerOLADer[FPB];
    float memDerOLAIzqFFT[FPB];
    float memIzqOLADer[FPB];
    float memIzqOLAIzqFFT[FPB];
    float memDerFFTnoOLA[FPB];
    float memIzqFFTnoOLA[FPB];
    float hanning[FPB];
    int flag;
}robotization_t;






void * prepareRobotization(void){
    robotization_t * p;
    p = malloc(sizeof(robotization_t));
    p->flag = 0;
    hanning(FPB, p->hanning, 0);

    return (void *) p;
}


void robotizationCall(const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate){
    robotization_t * uData = (robotization_t *) userData;
    float * memDerOLADer = uData->memDerOLADer;
    float * memDerOLAIzqFFT = uData->memDerOLAIzqFFT;
    float * memIzqOLADer = uData->memIzqOLADer;
    float * memIzqOLAIzqFFT = uData->memIzqOLAIzqFFT;
    float * memDerFFTcenter = uData->memDerFFTnoOLA;
    float * memIzqFFTcenter = uData->memIzqFFTnoOLA;
    float * hanning = uData->hanning;
    int flag = uData->flag;

    double auxCenterDer[FPB]; //los double se usaran para las funciones de FFT e IFFT
    double auxCenterIzq[FPB];
    float auxDerOLADer[FPB];
    float auxIzqOLADer[FPB];
   // float auxDerOLAIzq[FPB];
   // float auxIzqOLAIzq[FPB];
   // float auxDerOLAIzqFFT[FPB];
   // float auxIzqOLAIzqFFT[FPB];
    double auxDerComplexFFTCenter[FPB];
    double auxIzqComplexFFTCenter[FPB];
    double auxDerComplexFFTOLADer[FPB];
    double auxIzqComplexFFTOLADer[FPB];
    double auxDerOutReal[FPB];
    double auxDerOutIm[FPB];
    double auxIzqOutReal[FPB];
    double auxIzqOutIm[FPB];

    double memDerOLADer_auxFFT[FPB];
    double memIzqOLADer_auxFFT[FPB];

    int i;

    for(i = 0; i < framesPerBuffer; i++){
     //a la primer llamada del callback acomodo los valores inciales en cero.
        if(flag == 0){
            memDerOLADer[i] = 0;
            memIzqOLADer[i] = 0;
            memDerOLAIzqFFT[i] = 0;
            memIzqOLAIzqFFT[i] = 0;
            memDerFFTcenter[i] = 0;
            memIzqFFTcenter[i] = 0;
            
        }
        auxCenterDer[i] = 0; //los double se usaran para las funciones de FFT e IFFT
        auxCenterIzq[i] = 0;
        auxDerOLADer[i] = 0;
        auxIzqOLADer[i] = 0;
        //auxDerOLAIzq[i] = 0;
        //auxIzqOLAIzq[i] = 0;
        //auxDerOLAIzqFFT[i] = 0;
        //auxIzqOLAIzqFFT[i] = 0;
        auxDerComplexFFTCenter[i] = 0;
        auxIzqComplexFFTCenter[i] = 0;
        auxDerComplexFFTOLADer[i] = 0;
        auxIzqComplexFFTOLADer[i] = 0;
        auxDerOutReal[i] = 0;
        auxDerOutIm[i] = 0;
        auxIzqOutReal[i] = 0;
        auxIzqOutIm[i] = 0;
        
    }
    flag++;

    for(i=0; i < framesPerBuffer; i++){

        if(i < (framesPerBuffer/2)){ //voy llenando los viejos buffers del overlap derecho
            memDerOLADer[(FPB/2)+i] = in[2*i];
            memIzqOLADer[(FPB/2)+i] = in[(2*i)+1];
        }
        else if((i >= (framesPerBuffer/2)) && (i < framesPerBuffer)){ //voy preparando los que seran los nuevos buffers
            auxDerOLADer[i-(FPB/2)] = in[2*i];                  //derechos
            auxIzqOLADer[i-(FPB/2)] = in[(2*i)+1];
        }

        auxCenterDer[i] = (double) hanning[i]*in[2*i];  //voy aplicando hanning al buffer que proximamente sera central (audio derecho).
        auxCenterIzq[i] = (double) hanning[i]*in[(2*i)+1]; //idem para audio izquierdo.
        //printf("\n\n\n%f\n%f\n\n\n\n", auxCenterDer[i], hanning[i]);
        
        memDerOLADer[i] = hanning[i]*memDerOLADer[i]; //voy aplicando hanning al buffer de solapamiento derecho 
        memIzqOLADer[i] = hanning[i]*memIzqOLADer[i];

        memDerOLADer_auxFFT[i] = (double) memDerOLADer[i]; //ESTO ES PARA TRANSFORMAR CON ARREGLO DE DOUBLE EN LUGAR DE FLOAT
        memIzqOLADer_auxFFT[i] = (double) memIzqOLADer[i];
    }
    
    //printf("todo bien transformando...\n%f\n-----------------", auxCenterDer[10]);
    bool b = Fft_transform(memDerOLADer_auxFFT, auxDerComplexFFTOLADer, FPB); //hago fft del solapamiento derecho
    bool c = Fft_transform(memIzqOLADer_auxFFT, auxIzqComplexFFTOLADer, FPB);
    bool d = Fft_transform(auxCenterDer, auxDerComplexFFTCenter, FPB); //preparo la fft del buffer central para proximo uso
    bool e = Fft_transform(auxCenterIzq, auxIzqComplexFFTCenter, FPB);

    if(b && c && d && e){
        //
        //printf("todo bien transformando...\n%f\n", auxCenterDer[10]);
    }
    else{
        
    }

    for(i = 0; i < framesPerBuffer; i++){//AHORA TENGO QUE HACER FFT A MEMOLADER Y SUMAR CON LAS FFT CENTER Y MEMFFTOLAIZQ
        memDerOLADer[i] = (float) memDerOLADer_auxFFT[i]; //ESTO ES PARA VOLVER A FLOAT
        memIzqOLADer[i] = (float) memIzqOLADer_auxFFT[i];
        if(i < (framesPerBuffer/2)){
            auxDerOutReal[i] = ((double) memDerFFTcenter[i] + (double) memDerOLAIzqFFT[i+(FPB/2)]);
            auxIzqOutReal[i] = ((double) memIzqFFTcenter[i] + (double) memIzqOLAIzqFFT[i+(FPB/2)]);
        }
        else{
            auxDerOutReal[i] = ((double) memDerOLADer[i-(FPB/2)] + (double) memDerFFTcenter[i]);
            auxIzqOutReal[i] = ((double) memIzqOLADer[i-(FPB/2)] + (double) memIzqFFTcenter[i]);
        }
        
        auxDerOutIm[i] = 0.0; //AQUI ESTA EL EFECTO
        
        auxIzqOutIm[i] = 0.0;
    }
    //DESPUES TENGO QUE ANTITRANSFOMAR Y PONER EN LA SALIDA
    bool x = Fft_inverseTransform(auxDerOutReal, auxDerOutIm, FPB);
    bool y = Fft_inverseTransform(auxIzqOutReal, auxIzqOutIm, FPB);
    if(x && y){
        //printf("todo bien antitransformando...\n");
    }
    else{
        
    }
     for(i = 0; i < framesPerBuffer; i++){
         out[2*i] = (float) auxDerOutReal[i]/(FPB/1);
         out[(2*i)+1] = (float) auxIzqOutReal[i]/(FPB/1);

         if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
            out[2*i] = 0;
            out[(2*i)+1] = 0;
            
        }

         memDerOLAIzqFFT[i] = memDerOLADer[i]; //la vieja derecha es la nueva izquierda (con FFT hecha).
         memIzqOLAIzqFFT[i] = memIzqOLADer[i];

         memDerOLADer[i] = auxDerOLADer[i];     //la nueva derecha se actualiza (con FFT sin hacer aun).
         memIzqOLADer[i] = auxIzqOLADer[i];

         memDerFFTcenter[i] = (float) auxCenterDer[i];  //el centro se actualiza (con FFT hecha).
         memIzqFFTcenter[i] = (float) auxCenterIzq[i];
    } //DESPUES TENGO QUE PASAR MEMFFTOLADER A MEMFFTOLAIZQ, TENGO QUE PASAR EL NUEVO OLADER, TENGO QUE REEMPLAZAR EL FFTCENTER
    //CREO QUE DESPUES DE ESO YA ESTA TODO!!!


    uData->flag = flag; //esto es para registrar la cuenta del llenado de memoria
}

void refreshRobotization(int var1, int var2, void * p2effect){
    //robotization_t * pData = (robotization_t *) p2effect;
}
