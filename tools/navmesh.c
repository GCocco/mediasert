#include <stdio.h>
#include <stdlib.h>

int count = 0;

typedef struct{
  int x;
  int y;
}Coordinate;

typedef struct{
  int coll_start;
  int coll_end;
  struct y_obstacle* next;
}y_obstacle;


y_obstacle* append_obstacle(y_obstacle* obs, int start, int end){
  y_obstacle* new_node = NULL;
  
  new_node = (y_obstacle*) malloc(sizeof(y_obstacle));

  if (new_node == NULL){
    exit(-1);
  }
  
  new_node->next = NULL;
  
  new_node->coll_start = start;
  new_node->coll_end = end;
  

  if (obs == NULL){
    return new_node;
  }

  y_obstacle* head = obs;

  while(head->next != NULL){
    head = (y_obstacle*) head->next;
  }

  head->next = (struct y_obstacle*) new_node;
  return obs;
}

void _del_obstacle(y_obstacle* head){
  if (head->next!=NULL){
    _del_obstacle((y_obstacle*)head->next);
  }
  free(head);
  return;
}


typedef struct {
  int start;
  y_obstacle* obstacles;
  int end;
} abc_y;

typedef struct {
  int x_lines;
  int y_lines;
  double* x_coords;
  double* y_coords;
  abc_y* boundings;
} nav_mesh;


void _del_navmesh(nav_mesh* nm){
  free(nm->x_coords);
  free(nm->y_coords);
  for(int i=0; i<nm->x_lines; i++){
    if (nm->boundings[i].obstacles != NULL){
      _del_obstacle(nm->boundings[i].obstacles);
    }
  }
  free(nm->boundings);
  free(nm);
  printf("deleted navmesh from memory\n");
  return;
}

nav_mesh* newNavmesh(){
  nav_mesh* nm = (nav_mesh*) malloc(sizeof(nav_mesh));
}

void loadFromFile(nav_mesh* nm, char* filename){

  FILE* fp = NULL;
  int dumb1, dumb2, dumb3;
  
  fp = (FILE*) fopen(filename, "r");
  if (fp == NULL){
    printf("Can't open file %s\n", filename);
    return;
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
  return;
}

void check(nav_mesh* nm){
  printf("%d, %d\n", nm->x_lines, nm->y_lines);
  printf("sembra tutto ok\n");
  return;
}

Coordinate find(nav_mesh*nm, double x, double y){
  Coordinate c;
  int i = 0;
  printf("%lf\n", nm->x_coords[0]);
  printf("%lf\n", x);
  
  while (nm->x_coords[i] < x &&  i<nm->x_lines){
    i++;
  }
  c.x = i;
  i = 0;
  while (nm->y_coords[i] < y && i<nm->y_lines){
    i++;
  }
  c.y = i;

  printf("%d, %d\n", c.x, c.y);
  return c;
}


int main(){
  printf("initializing navmesh statics...\n");
  
  nav_mesh* nm = newNavmesh();
  loadFromFile(nm, "./mynavmesh.csv");
  Coordinate c;
  
  c = find(nm, (double)-10.0, (double)100.0);
  
  return 0;
}


