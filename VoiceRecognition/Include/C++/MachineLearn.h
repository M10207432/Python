//#include "Python.h"


/*======================
	Configuration
======================*/

#define InputNum 50
#define HiddenNum 50
#define OutputNum 50

#define EndVal 100
/*======================
		Structure
======================*/
typedef enum {
	input,
	output,
	hidden,
}node_type;

typedef struct _node{
	int id;							//Node id
	int layer_id;				//Node Layer id
	node_type type;	//node type {input, outpu, hidden}

	double value;
	double threshold;	
		
	struct _node* next;
	struct _node* pre;
}Node;

/*======================
	Function Prototype
======================*/

/*
PyObject* SqrtInPyObj(PyObject* obj);
double GetInput(PyObject* list);
*/
double* MatrixEvaluate(double* input, double *hiddenNode, double *Hidden_th);

/*======================
		Test
======================*/
double Add(double n1, double n2);
float Div(float n, float div);

