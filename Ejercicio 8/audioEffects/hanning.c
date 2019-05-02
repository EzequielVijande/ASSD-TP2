#include "hanning.h"
#include "math.h"
#include "stdio.h"


void hanning(int N, float * w, short itype)
{
    int half, i, idx, n;

    if(itype==1)    //periodic function
        n = N-1;
    else
        n = N;

    if(n%2==0)
    {
        half = n/2;
        for(i=0; i<half; i++){ //CALC_HANNING   Calculates Hanning window samples.
            w[i] = (0.5) * (1.0 - cos(2.0*((M_PI)*((i+1)) / ((n+1)))));
        }
        idx = half-1;
        for(i=half; i<n; i++) {
            w[i] = w[idx];
            idx--;
        }
    }
    else
    {
        half = (n+1)/2;
        for(i=0; i<half; i++) //CALC_HANNING   Calculates Hanning window samples.
            w[i] = 0.5 * (1 - cos(2*M_PI*(i+1) / (n+1)));

        idx = half-2;
        for(i=half; i<n; i++) {
            w[i] = w[idx];
            idx--;
        }
    }

    if(itype==1)    //periodic function
    {
        for(i=N-1; i>=1; i--)
            w[i] = w[i-1];
        w[0] = 0.0;
    }
}