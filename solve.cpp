#include "Game.h"
#include <iostream>
#include <Python.h>
#include <string>
#include <vector>


const std::string solve(const std::vector<int> &board) {
std::cout << "solve" << std::endl;
  Py_Initialize();

  PyObject *typingModule = PyImport_ImportModule("typing");
  if (!typingModule) {
    PyErr_Print();
  }

  PyObject *heapqModule = PyImport_ImportModule("heapq");
  if (!heapqModule) {
    PyErr_Print();
  }

  PyObject *mathModule = PyImport_ImportModule("math");
  if (!mathModule) {
    PyErr_Print();
  }

  PyObject *sysModule = PyImport_ImportModule("sys");
  if (!sysModule) {
    PyErr_Print();
  }

  PyObject *dequeModule = PyImport_ImportModule("deque");
  if (!dequeModule) {
    PyErr_Print();
  }

  const char *path = "./";
  wchar_t *wpath = Py_DecodeLocale(path, NULL);
  if (wpath != NULL) {
    PySys_SetPath(wpath);
    PyMem_RawFree(wpath);
  }
  PyObject *tilesModule = PyImport_ImportModule("tiles");
  std::cout << "imported" << std::endl;
  if (tilesModule != NULL) {
    // Get the main function
    PyObject *mainFunc = PyObject_GetAttrString(tilesModule, "solvePuzzle");
std::cout << "got main" << std::endl;
    if (mainFunc && PyCallable_Check(mainFunc)) {
      // Create a tuple for the arguments - the current board
      PyObject *pyList = PyList_New(0); // create a new empty Python list
      std::cout<<SIZE<<std::endl;
      // parse the puzzle board into a Python list
      for (int i = 0; i < SIZE; i++) {
        PyObject *pyInt = PyLong_FromLong(board[i]);
        PyList_Append(pyList, pyInt);
        Py_DECREF(pyInt);
      }

      // now you can pass pyList to your Python function
      PyObject *result = PyObject_CallFunctionObjArgs(mainFunc, pyList, NULL);

      // Check if the call succeeded
      if (result != NULL) {
        path = PyUnicode_AsUTF8(PyObject_Str(result));
        std::cout << "done " << path << std::endl;
        return path;
        Py_DECREF(result);
      } else {
        PyErr_Print();
      }

      Py_DECREF(pyList);
      Py_DECREF(mainFunc);
    } else {
      if (PyErr_Occurred()) {
        PyErr_Print();
      }
    }

    Py_DECREF(tilesModule);
    Py_DECREF(typingModule);
    Py_DECREF(heapqModule);
    Py_DECREF(mathModule);
    Py_DECREF(sysModule);
  } else {
    PyErr_Print();
  }

  Py_Finalize();
  return path;
}