#ifndef VoiceWindow_H
#define VoiceWindow_H

void PreEmphasis(double *);
void FrameBlock(double *);	
void FilterBank( double *Mel, double *Energy, int size);
void Cepstrum(double *);

#endif
