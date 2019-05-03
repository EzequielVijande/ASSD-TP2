//effectStructs.h
//This file contain the structures of the audio effects, having into account the parameters
//that define the caracteristics of each one.

#ifndef EFFECTSTRUCTS_H
#define EFFECTSTRUCTS_H

//EFFECTS AVAILABLE FOR THE USER:
#define REVERB_ALLPASS 0 //primer efecto
#define ECHO_SIMPLE 1
#define REVERB_PLANE 2
#define REVERB_LOWPASS 3
#define REVERB_COMPLETE 4
#define REVERB_CONVOLUTION 5
#define ROBOTIZATION 6
#define HEADPHONES3D 7
#define VIBRATO 8
#define FLANGER 9     //ultimo efecto



#define FPB 64

typedef int EFFECT_TYPE;
typedef float SAMPLE;


typedef struct {
    
    void * p2effect;

    void (*destroyEffect)(void * ptr);

    void (*p2callback) (const SAMPLE * in, SAMPLE * out, unsigned long framesPerBuffer, void * userData, int sampleRate);

    void (*p2refresh) (int var1, int var2, void * p2effect);

}audioEffectsParameters_t;

#endif //EFFECTSTRUCTS_H