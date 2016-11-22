#ifndef VoiceWindow_H
#define VoiceWindow_H

void PreEmphasis(double *);
void FrameBlock(double *data, int frame_id, int frame_end);	
void FilterBank( double *Mel, double *Energy, int size);
void Cepstrum(double *);
void Delta_Cepstrum(double *);

#endif
