//effects.c
//backend

#include "effects.h"
#include "effectStructs.h"
#include "stdio.h"
#include "math.h"
#include "fftC.h"

//bool Fft_transform(double real[], double imag[], size_t n);
//bool Fft_inverseTransform(double real[], double imag[], size_t n);

#define L 20000
#define M 400
#define F 7
#define B 200//
#define E 5800
#define G 0.7
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
    audioEffectsParameters_t * uData = (audioEffectsParameters_t *) userData;
    float * memDerOLADer = (uData->robotization).memDerOLADer;
    float * memDerOLAIzqFFT = (uData->robotization).memDerOLAIzqFFT;
    float * memIzqOLADer = (uData->robotization).memIzqOLADer;
    float * memIzqOLAIzqFFT = (uData->robotization).memIzqOLAIzqFFT;
    float * memDerFFTcenter = (uData->robotization).memDerFFTnoOLA;
    float * memIzqFFTcenter = (uData->robotization).memIzqFFTnoOLA;
    float * hanning = (uData->robotization).hanning;
    int flag = (uData->robotization).flag;

    double auxCenterDer[FPB]; //los double se usaran para las funciones de FFT e IFFT
    double auxCenterIzq[FPB];
    float auxDerOLADer[FPB];
    float auxIzqOLADer[FPB];
    float auxDerOLAIzq[FPB];
    float auxIzqOLAIzq[FPB];
    float auxDerOLAIzqFFT[FPB];
    float auxIzqOLAIzqFFT[FPB];
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

    int i, j, m;

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
        auxDerOLAIzq[i] = 0;
        auxIzqOLAIzq[i] = 0;
        auxDerOLAIzqFFT[i] = 0;
        auxIzqOLAIzqFFT[i] = 0;
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
        printf("algo mal transformando\n");
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
        printf("algo mal antitransformando\n");
    }
     for(i = 0; i < framesPerBuffer; i++){
         out[2*i] = (float) auxDerOutReal[i]/(FPB/1);
         out[(2*i)+1] = (float) auxIzqOutReal[i]/(FPB/1);

         if((out[2*i] < -1) || (out[2*i] > 1)  || (out[(2*i)+1] < -1) || (out[(2*i)+1] > 1) ){
             printf("%f\n%f\n", out[2*i], out[(2*i)+1]);
            out[2*i] = 0;
            out[(2*i)+1] = 0;
            printf("problemita de normalizacion o de error numerico\n");
        }

         memDerOLAIzqFFT[i] = memDerOLADer[i]; //la vieja derecha es la nueva izquierda (con FFT hecha).
         memIzqOLAIzqFFT[i] = memIzqOLADer[i];

         memDerOLADer[i] = auxDerOLADer[i];     //la nueva derecha se actualiza (con FFT sin hacer aun).
         memIzqOLADer[i] = auxIzqOLADer[i];

         memDerFFTcenter[i] = (float) auxCenterDer[i];  //el centro se actualiza (con FFT hecha).
         memIzqFFTcenter[i] = (float) auxCenterIzq[i];
    } //DESPUES TENGO QUE PASAR MEMFFTOLADER A MEMFFTOLAIZQ, TENGO QUE PASAR EL NUEVO OLADER, TENGO QUE REEMPLAZAR EL FFTCENTER
    //CREO QUE DESPUES DE ESO YA ESTA TODO!!!


    (uData->robotization).flag = flag; //esto es para registrar la cuenta del llenado de memoria
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
