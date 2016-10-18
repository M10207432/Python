#include "Python.h"

/*======================
	Configuration
======================*/

#define InputNum 50
#define HiddenNum 50
#define OutputNum 50

/*======================
		Structure
======================*/

typedef struct _hiddennode{
	int id;			//HiddenNode id
	int layer_id;		//HiddenNode Layer id
	
	double threshold;	
	
	double output;
	double Err;
	
	struct _hiddennode* next;
	struct _hiddennode* pre;
}HiddenNode;

/*======================
	Function Prototype
======================*/

double GetInput(PyObject* list);
void weightEvaluate(int start, int end_id, struct _hiddennode* node);


/*======================
		Test
======================*/
double Add(double n1, double n2);
float Div(float n, float div);


PyObject* SqrtInPyObj(PyObject* obj);