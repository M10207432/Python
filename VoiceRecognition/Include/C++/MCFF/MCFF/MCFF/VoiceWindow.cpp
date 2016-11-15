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
	
	unsigned int frame_idx=0;
	double Hamming_Wid=0;

	do{

		//Evaluate for each Window
		for(int k=0; k<FFT_K && (k+frame_idx)<FrameSample; k++){
			 std::complex<double> sum(0.0,0.0);	// complex(Real,Img)

			 //Evaluate for each FFT (0~N)
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

void FilterBank(double *data){
	double mel_lower_freq=1125*log(1+Lower_Freq/700);
	double mel_upper_freq=1125*log(1+Upper_Freq/700);
	double mel_f[FilterBank_Num+2];
	double BIN[FilterBank_Num+2];

	//Transfer to Mel Frequence
	for(int i=0; i<FilterBank_Num+2; i++){
		mel_f[i]=mel_lower_freq+((mel_upper_freq-mel_lower_freq)/(FilterBank_Num+1))*i;
		mel_f[i]=700*(exp(mel_f[i]/1125)-1);

		//FFT BIN [f(i) = floor((nfft+1)*h(i)/samplerate)]
		BIN[i]=floor(FFT_K*mel_f[i]/FrameSample);
	}

	//Through Filter
	for(int i=0; i<FilterBank_Num+1; i++){
		static double F_pre,F_m,F_post;
		
		//Find the filter id
		if(i==0){
			F_pre=0;
			F_m=BIN[i];
			F_post=BIN[i+1];
		}else{
			F_pre=BIN[i-1];
			F_m=BIN[i];
			F_post=BIN[i+1];
		}

		//
		for(int k=0; k<FFT_K; k++){
			if(FFT_Output[k]<F_pre){

				MCFF[i][k]=0;

			}else if (FFT_Output[k] >= F_pre && FFT_Output[k]<F_m){

				MCFF[i][k]=(FFT_Output[k]-F_pre)/(F_m-F_pre);

			}else if (FFT_Output[k] >= F_m && FFT_Output[k]<F_post){

				MCFF[i][k]=(F_post-FFT_Output[k])/(F_post-F_m);

			}else if (FFT_Output[k] >= F_post){

				MCFF[i][k]=0;

			}
		}

	}
	


}