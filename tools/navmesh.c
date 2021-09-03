#define PY_SSIZE_T_CLEAN

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include <assert.h>
#include <stdlib.h>

void main(){
  FILE * fp = (FILE*) fopen("mynavmesh.csv", "r");
  int x_num, y_num;
  int dumb = 0;
  int dumb2 = 0;
  
  fscanf(fp, "%d,%d\n", &x_num, &y_num);
  printf("x lines: %d\n", x_num);
  printf("x_lines: %d\n", y_num);

  double x_coords[x_num];
  double y_coords[y_num];
  
  printf("Reading grid coordinates:\n");
  
  for (int i=0; i<x_num; i++){
    fscanf(fp, "%lf,", &x_coords[i]);
    printf("%lf ", x_coords[i]);
  }

  fscanf(fp, "\n");
  printf("\n");
  for (int i=0; i<y_num; i++){
    fscanf(fp, "%lf,", &y_coords[i]);
    printf("%lf ", y_coords[i]);
  }
  
  printf("\n");
  printf("loading colliders\n");

  for (int i=0; i<x_num; i++){
    fscanf(fp, "%d, ", &dumb);
    for (int j=0; j<(dumb * 2) + 2; j++){
      fscanf(fp, "%d,", &dumb2);
      printf("%d ", dumb2);
    }
    printf("\n");
  }

  
  fclose(fp);
  
}
