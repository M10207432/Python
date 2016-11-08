#include "VoiceWindow.h"
#include "Config.h"
#include <math.h>

/*====================
				Signal pass through 
					High Pass Filter
s2(n) = s(n) - PreEmp_gain*s(n-1) 
(0.8<PreEmp_gain<0.9)
====================*/
void PreEmphasis(double *data){

	for(int i=1; i<FrameSample; i++){
		*(PreEmp_Output+i)=*(data+i)-(*(data+i-1))*PreEmp_gain;
	}

}

/*=============================
			<Frame Block & Hamming Block>
		For getting N point as one frame
		There would have M points overlay
(Signal Sampling freq is 8KHZ~16KHZ)
(N 256 or 512)
=============================*/
void FrameBlock(double *data){
	double Hamming_Wid=0;

	for(int i=0; i<FrameSample; i=i+Frame_N){
		for(int j=0; j<Frame_N; j++){
			Hamming_Wid=(1-Hamming_gain)-Hamming_gain*cos((2*PI*j)/(Frame_N-1));
			Hamming_Output[i+j]=Hamming_Wid*data[i+j];
		}
	}
}


