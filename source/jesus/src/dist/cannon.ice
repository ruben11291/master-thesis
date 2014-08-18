// No editar este fichero (vinculado al documento)

#include <Ice/BuiltinSequences.ice>

module Cannon {
  struct Matrix {
    int ncols;
    Ice::DoubleSeq data;
    string UUID;
  };

  interface Operations {
    Matrix matrixMultiply(Matrix a, Matrix b);
  };

  interface Collector {
    void injectSubmatrix(Matrix m, int row, int col);
  };

  interface Processor {
    void init(int row, int col, Processor* above, Processor* left,
              int order, Collector* target);
    void injectFirst(Matrix a, int step);
    void injectSecond(Matrix b, int step);
  };
};
