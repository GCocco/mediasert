#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include <assert.h>
#include <stdlib.h>


typedef struct{
  int coll_start;
  int coll_end;
  struct y_obstacle* next;
}y_obstacle;   //ok

typedef struct {
  int start;
  y_obstacle* obstacles;
  int end;
} abc_y;      //

typedef struct {
  int x_lines;
  int y_lines;
  double* x_coords;
  double* y_coords;
  abc_y* boundings;
} nav_mesh;

y_obstacle* append_obstacle(y_obstacle* obs, int start, int end){
  y_obstacle* new_node = NULL;

  new_node = (y_obstacle*) malloc(sizeof(y_obstacle));
  if (new_node == NULL){
    printf("lmao voglio morire");
  }
  
  new_node->next = NULL;
  
  new_node->coll_start = start;
  new_node->coll_end = end;
  

  if (obs == NULL){
    return new_node;
  }

  y_obstacle* head = obs;

  while(head->next != NULL){
    head = (y_obstacle*) head-> next;
  }

  head->next = (struct y_obstacle*) new_node;
  return obs;
}

nav_mesh load_from_file(char* filename, nav_mesh* nm){
  FILE* fp = NULL;
  int dumb1, dumb2, dumb3;
  fp = (FILE*) fopen(filename, "r");
  if (fp == NULL){
    printf("AAAAAAAAAAAAAAAAAAA");
  }

  fscanf(fp, "%d, %d\n", &nm->x_lines, &nm->y_lines);
  nm->x_coords = (double*) calloc(nm->x_lines, sizeof(double));
  for (int i=0; i<nm->x_lines; i++){
    fscanf(fp, "%lf,", &nm->x_coords[i]);
  }
  
  nm->y_coords = (double*) calloc(nm->y_lines, sizeof(double));
  for (int i=0; i<nm->x_lines; i++){
    fscanf(fp, "%lf,", &nm->y_coords[i]);
  }

  
  nm->boundings = calloc(nm->x_lines, sizeof(abc_y));


  
  for(int i = 0; i<nm->x_lines; i++){
    fscanf(fp, "%d,", &dumb1);

    nm->boundings[i].obstacles = NULL;
    
    fscanf(fp, "%d,", &nm->boundings[i].start);
    
    for(int j = 0; j<dumb1; j++){
      fscanf(fp, "%d,%d,", &dumb2, &dumb3);
      nm->boundings[i].obstacles = append_obstacle(nm->boundings[i].obstacles, dumb2, dumb3);
    }
    fscanf(fp, "%d\n", &nm->boundings[i].end);
  }
  fclose(fp);
}




void main(){
  nav_mesh culo;
  load_from_file("mynavmesh.csv", &culo);


  if (0){
    printf("x lines: %d \ny lines: %d\n", culo.x_lines, culo.y_lines);
    printf("\nx coordinates: \n");
    for (int i = 0; i < culo.x_lines; i++){
      printf("%lf\n", culo.x_coords[i]);
    }
  }
  if (0){
    printf("\ny coordinates: \n");
    for(int i = 0; i< culo.y_lines; i++){
      printf("%lf\n", culo.y_coords[i]);
    }
  }
  if (1){
    printf("\nboundings:\n");
    for (int i = 0; i< culo.x_lines; i++){

      
      printf("%d", culo.boundings[i].start);
      y_obstacle* head = culo.boundings[i].obstacles;
      while (head != NULL){
	printf(" {%d, %d}", head->coll_start, head->coll_end);
	head = (y_obstacle*)head->next;
      }
      printf(" %d\n", culo.boundings[i].end);	
    }
  }
  
}
