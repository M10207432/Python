#include "VoiceWindow.h"
#include "Config.h"
#include <math.h>
#include <complex>

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
		for(int k=0; k<Frame_N && (k+frame_idx)<FrameSample; k++){
			 std::complex<double> sum(0.0,0.0);	// complex(Real,Img)

			 //Evaluate for each FFT (0~K)
			for(int n=0; n<Frame_N && (n+frame_idx)<FrameSample; n++){

				Hamming_Wid=(1-Hamming_gain)-Hamming_gain*cos((2*PI*n)/(Frame_N-1));
				std::complex<double> exp_pow(0.0,( -2*PI*k*n)/Frame_N);		// complex(Real,Img)
				
				sum=(data[n+frame_idx])*Hamming_Wid*exp(exp_pow);		
			}

			FFT_Output[k+frame_idx]=(abs(sum)*abs(sum))/Frame_N;
		}

		//For next Window
		frame_idx=frame_idx+Frame_N-Frame_M;

	}while(frame_idx<FrameSample);

}

