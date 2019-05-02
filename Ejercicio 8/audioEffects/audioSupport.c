//audioSupport.c

#include "audioSupport.h"
#include "effectStructs.h"
#include "effects.h"
#include "portaudio.h"
#include "stdlib.h"
#include "stdio.h"

//#include "effectSupport.h"



#define SAMPLE_RATE         (44100)
#define PA_SAMPLE_TYPE      paFloat32
#define FRAMES_PER_BUFFER   (FPB)

typedef float SAMPLE;


static int PAcallback( const void *inputBuffer, void *outputBuffer,
                         unsigned long framesPerBuffer,
                         const PaStreamCallbackTimeInfo* timeInfo,
                         PaStreamCallbackFlags statusFlags,
                         void *userData );

////////////////////////////////////////

audioSupportResults_t implementAudioEffects(int effect, void * userData){
    selectCallback(userData, effect); ///////
    
    audioSupportResults_t result;
    result.succeded = true;
    result.errorMessage = "Any problem installing audio support";
    PaStreamParameters inputParameters, outputParameters;
    PaStream *stream;
    PaError err;

    err = Pa_Initialize();
    if( err != paNoError ){
        result.succeded = false;
        result.errorMessage = "Problems with Audio Support Installation, sorry.\n"; //Pa_GetErrorText( err )
        result.errorNumber = (int) err;
        return result;
    }

    inputParameters.device = Pa_GetDefaultInputDevice(); /* default input device */
    if (inputParameters.device == paNoDevice) {
        result.succeded = false;
        result.errorMessage = "Error: No default input device.\n";
        return result; 
    }
    
    inputParameters.channelCount = 2;       /* stereo input */
    inputParameters.sampleFormat = PA_SAMPLE_TYPE;
    inputParameters.suggestedLatency = Pa_GetDeviceInfo( inputParameters.device )->defaultLowInputLatency;
    inputParameters.hostApiSpecificStreamInfo = NULL;

    outputParameters.device = Pa_GetDefaultOutputDevice(); /* default output device */
    if (outputParameters.device == paNoDevice) {
      result.errorMessage = "Error: No default output device.\n";
      result.succeded = false;
      return result;
    }

    outputParameters.channelCount = 2;       /* stereo output */
    outputParameters.sampleFormat = PA_SAMPLE_TYPE;
    outputParameters.suggestedLatency = Pa_GetDeviceInfo( outputParameters.device )->defaultLowOutputLatency;
    outputParameters.hostApiSpecificStreamInfo = NULL;

    err = Pa_OpenStream(
              &stream,
              &inputParameters,
              &outputParameters,
              SAMPLE_RATE,
              FRAMES_PER_BUFFER,
              0, /* paClipOff, */  /* we won't output out of range samples so don't bother clipping them */
              PAcallback,
              userData);
    if( err != paNoError )
    {
        result.succeded = false;
        result.errorMessage = "Error opening the stream, sorry \n"; 
        result.errorNumber = (int) err;
        return result;
    }

    err = Pa_StartStream( stream );
    if( err != paNoError ){
        result.succeded = false;
        result.errorMessage = "Error starting the stream \n";
        result.errorNumber = (int) err;
        return result;
    }
    result.pDataSupport = stream;
    return result;
}

audioSupportResults_t uninstallAudioEffects(void * pDataSupport){
    PaStream *stream = pDataSupport;
    PaError err;
    audioSupportResults_t result;
    result.succeded = true;
    result.errorMessage = "Any Problem Closing Audio Support\n";
    result.pDataSupport = NULL;
    err = Pa_CloseStream( stream );
    if( err != paNoError ){
        result.succeded = false;
        result.errorMessage = "Problems closing audio support...\n";
        result.errorNumber = (int) err;
        return result;
    }
    Pa_Terminate();
    return result;
}   





/////////////////////////////

static int PAcallback( const void *inputBuffer, void *outputBuffer,
                         unsigned long framesPerBuffer,
                         const PaStreamCallbackTimeInfo* timeInfo,
                         PaStreamCallbackFlags statusFlags,
                         void *userData )
{
    SAMPLE *out = (SAMPLE*)outputBuffer;
    const SAMPLE *in = (const SAMPLE*)inputBuffer;
    unsigned int i;
    (void) timeInfo; /* Prevent unused variable warnings. */
    (void) statusFlags;
    audioEffectsParameters_t * userData_cast = (audioEffectsParameters_t *) userData;

    if( inputBuffer == NULL )
    {
        for( i=0; i<framesPerBuffer; i++ )
        {
            *out++ = 0;  /* left - silent */
            *out++ = 0;  /* right - silent */
        }
    }
    else
    {
        userData_cast->p2callback(in, out, framesPerBuffer, userData, SAMPLE_RATE);
    }
    
    return paContinue;
}