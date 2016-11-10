#ifndef CONFIG_H
#define CONFIG_H

#define SignalFreq 16000 //16KHZ (8KHZ)
#define FrameSample 16000 //16KHZ (8KHZ)
#define PI 3.14159265
/*-------------------------------
			VoiceWindow
-------------------------------*/
#define PreEmp_Size 100
#define PreEmp_gain 0.95

#define FrameInterval 0.025
#define OverlapInterval 0.01
#define Frame_N (SignalFreq*FrameInterval)
#define Frame_M (SignalFreq*OverlapInterval)
#define Hamming_gain 0.46

double PreEmp_Output[FrameSample];
double FFT_Output[FrameSample];

#endif