#include "Python.h"

int AddOne(int n);
int Sqrt(int n);
double Add(double n1, double n2);
float Div(float n, float div);

PyObject* SqrtInPyObj(PyObject* obj);