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
			<Frame Block with Hamming Block & FFT>
		For getting N point as one frame
		There would have M points overlay
(Signal Sampling freq is 8KHZ~16KHZ)
(N 256 or 512)
=============================*/
void FrameBlock(double *data){
	
	int frame_idx=0;
	double Hamming_Wid=0;
	double sum=0;

	do{

		//Evaluate for each Window
		for(int k=frame_idx; k<Frame_N+frame_idx; k++){
			for(int n=frame_idx; n<Frame_N+frame_idx; n++){
				if(n>=FrameSample){
					continue;
				}
				Hamming_Wid=(1-Hamming_gain)-Hamming_gain*cos((2*PI*n)/(Frame_N-1));
				sum=Hamming_Wid*data[n]*exp((-2*PI*k*n)/Frame_N)+sum;		
			}
			if(k>=FrameSample){
					break;
			}
			FFT_Output[k]=sum;
		}

		//For next Window
		frame_idx=frame_idx+Frame_N-Frame_M;


	}while(frame_idx<FrameSample);

}

