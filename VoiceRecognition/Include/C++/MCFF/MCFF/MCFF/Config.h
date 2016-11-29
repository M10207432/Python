#ifndef CONFIG_H
#define CONFIG_H

#define FrameSample 16000 //16KHZ (8KHZ)
#define PI 3.14159265
/*-------------------------------
			VoiceWindow
-------------------------------*/
#define PreEmp_Size 100
#define PreEmp_gain 0.95

#define FrameInterval 0.025
#define OverlapInterval 0.01

#define Frame_N 400 //FrameSample*FrameInterval
#define Frame_M 160 //FrameSample*OverlapInterval

#define Hamming_gain 0.46
#define FFT_K 400

#define FilterBank_Num 24
#define Mel_L 12
#define Delta_M 2
#define Lower_Freq 300
#define Upper_Freq 8000

double PreEmp_Output[FrameSample];
double FFT_Output[FrameSample];
double DFT_Energy[FrameSample];

double MFCC[Mel_L];
double Delta_Cep[Delta_M*Mel_L];

#endif