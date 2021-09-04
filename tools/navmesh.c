#include <stdio.h>
#include <stdlib.h>

int count = 0;

typedef struct{
  int coll_start;
  int coll_end;
  struct y_obstacle* next;
}y_obstacle;

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

nav_mesh ** navmesh_map = NULL;
int navmesh_counter = 0;

int new_navmesh(){  
  if (navmesh_counter==0){
    navmesh_map = (nav_mesh**) calloc(1, sizeof(nav_mesh*));
  }
  else{
    navmesh_map = (nav_mesh**) realloc(navmesh_map, (navmesh_counter+1) * sizeof(nav_mesh*));
  }
  navmesh_map[navmesh_counter] = (nav_mesh*) malloc(sizeof(nav_mesh));
  return (++navmesh_counter);
}

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

int load_from_file(char* filename){

  
  FILE* fp = NULL;
  int dumb1, dumb2, dumb3;


  int index = new_navmesh();


  nav_mesh* nm = navmesh_map[index-1];

  printf("%s", filename);
  
  fp = (FILE*) fopen(filename, "r");
  if (fp == NULL){
    return -1;
  }

  printf("AAAAAAAAAAAAAAAAAAAAAAAAAA");

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
  return index;
}

void check(){
  printf("sembra tutto ok\n");
  return;
}

void ayy_lmao(int nm_index){
  printf("navcount: %d\n", navmesh_counter);
  printf("mycount: %d\n", nm_index);

  printf("%p\n", navmesh_map);
  printf("%d, %d\n", navmesh_map[nm_index]->x_lines, navmesh_map[nm_index]->y_lines);
  return;
}


int main(){
  printf("initializing navmesh statics...\n");
  
  int ind = load_from_file("./mynavmesh.csv");
  
  printf("%d\n", ind);


  ayy_lmao(0);
  
  return 0;
}
