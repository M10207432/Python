//#include "Python.h"

/*======================
		Structure
======================*/


typedef struct _node{
	int id;							//Node id
	int layer_id;				//Node Layer id

	double weight;
	double value;
	double threshold;	
	double error;	

	struct _node* next;
	struct _node* pre;
}Node;

/*======================
	Configuration
======================*/

#define InputNum 2
#define HiddenNum 10
#define OutputNum 1

#define SetNum 5

#define init_weight 0.1
#define init_th 0.1

#define FileSIZE 100
#define RandRng 100

#define alpha_weight 0.9

#define default_setting 0
/*======================
	Function Prototype
======================*/

/*
PyObject* SqrtInPyObj(PyObject* obj);
double GetInput(PyObject* list);
*/


void MatrixEvaluate(double* , double *, double *);
void ErrorEvaluate(int );
void ReviseWeight(int );

void AssignHiddenNode();
void AssignIO(char *);

void RUN();

/*======================
		Test
======================*/
double Add(double n1, double n2);
float Div(float n, float div);

