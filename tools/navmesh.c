#include  <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int count = 0;

typedef struct{
  int x;
  int y;
}Coordinate;



/**
DEFINIZIONE NAVMESH 
 **/
typedef struct{
  int coll_start;
  int coll_end;
  struct y_obstacle* next;
}y_obstacle;


y_obstacle* __append_obstacle(y_obstacle* obs, int start, int end){
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

void __del_obstacle(y_obstacle* head){
  if (head->next!=NULL){
    __del_obstacle((y_obstacle*)head->next);
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
      __del_obstacle(nm->boundings[i].obstacles);
    }
  }
  free(nm->boundings);
  free(nm);
  printf("deleted navmesh from memory\n");
  return;
}

nav_mesh* __newNavmesh(){
  nav_mesh* nm = (nav_mesh*) malloc(sizeof(nav_mesh));
}

void __loadFromFile(nav_mesh* nm, char* filename){

  FILE* fp = NULL;
  int dumb1, dumb2, dumb3;
  
  fp = (FILE*) fopen(filename, "r");
  if (fp == NULL){
    printf("Can't open file %s\n", filename);
    exit(-1);
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
      nm->boundings[i].obstacles = __append_obstacle(nm->boundings[i].obstacles, dumb2, dumb3);
    }
    fscanf(fp, "%d\n", &nm->boundings[i].end);
  }
  fclose(fp);
  return;
}

nav_mesh* newNavmesh(char* filename){
  nav_mesh* nm = __newNavmesh();
  __loadFromFile(nm, filename);
  return nm;
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

bool __can_walk(nav_mesh* nm, Coordinate c){
  if (nm->boundings[c.x].start > c.y || nm->boundings[c.x].end < c.y){
    return false;
  }
  if (nm->boundings[c.x].obstacles == NULL){
    return true;
  }
  y_obstacle* ob = nm->boundings[c.x].obstacles;

  while(ob){
    if (ob->coll_end > c.y){
      if (ob->coll_start < c.y){
	return false;
      }
      ob = (y_obstacle*)ob->next;
    }
    else{
      return true;
    }
  }
  return true;
}


/**
RICERCA PERCORSO
**/


typedef struct{  // struct for a list/set of nodes
  Coordinate coord;
  struct grid_node* next;
}grid_node;

typedef struct{  // struct for a list of nodes containing the shortest path to self the distance of said path
  Coordinate coord;
  float tot_distance;
  struct path_node* previous;
  struct path_node* next;
}path_node;

typedef struct{  // struct for a list of nodes 
  Coordinate coord;
  double distance;
  struct unvisited_node* next;
}unvisited_node;



unvisited_node* new_unvisited(Coordinate c, Coordinate end){
  unvisited_node* un = malloc(sizeof(unvisited_node));
  un->coord.x = c.x;
  un->coord.y = c.y;
  un->next = NULL;
  un->distance = sqrt(pow((double)c.x - (double)end.x, 2) +
		      pow((double)c.y - (double)end.y, 2));
  return un;
}


unvisited_node* append_sorted(unvisited_node* list, unvisited_node* node){
  unvisited_node* current = NULL;
  unvisited_node* last = NULL;
  
  if (list == NULL){
    return node;
  }
  current = (unvisited_node*) list->next;
  last = list;

  while(current){
    if (current->distance > node->distance){
      node->next = (struct unvisited_node*) current;
      last->next = (struct unvisited_node*) node;
      return list;
    }
    
  }
  last->next = (struct unvisited_node*) node;
  return list;
}

bool buffered(unvisited_node* list, Coordinate c){
  unvisited_node* current;
  while (current!= NULL){
    if (current->coord.x == c.x && current->coord.y == c.y){
      return true;
    }
  }
  return false;
}

bool parsed(path_node* path, Coordinate c){
  path_node* current;
  while (current!= NULL){
    if (current->coord.x == c.x && current->coord.y == c.y){
      return true;
    }
  }
  return false;
}



void a_star(nav_mesh* nm, Coordinate start, Coordinate end){
  path_node* closed = NULL;
  unvisited_node* open = NULL;
  Coordinate adj;
  unvisited_node* current;
  path_node* new_pn;
  
  closed = (path_node*) malloc(sizeof(path_node));
  closed->coord.x = start.x;
  closed->coord.y = start.y;
  closed->tot_distance = (double)0.0;
  closed->previous = NULL;
  closed->next = NULL;
  
  /// aggiungo i primi 8 nodi al buffer (se percorribili)
  adj.x = start.x - 1;
  adj.y = start.y;
  if (__can_walk(nm, adj)){
    open = append_sorted(open, new_unvisited(adj, end));
  }
  adj.x = start.x + 1;
  if (__can_walk(nm, adj)){
    open = append_sorted(open, new_unvisited(adj, end));
  }
  adj.x = start.x;
  adj.y = start.y - 1;
  if (__can_walk(nm, adj)){
    open = append_sorted(open, new_unvisited(adj, end));
  }
  adj.y = start.y + 1;
  if (__can_walk(nm, adj)){
    open = append_sorted(open, new_unvisited(adj, end));
  }


  while(open != NULL){
    current = open;
    open = current->next;
    
    if (current->coord.x == end.x && current->coord.y ==end.y){
      ///se il nodo è il nodo destinazione
      //libera la memoria e restituisci il percorso
    }
    new_pn = (path_node*) malloc(sizeof(path_node));
    new_pn->coord.x = current->coord.x;
    new_pn->coord.y = current->coord.y;
    // new_pn->previous = Come ottengo l'equivalente di 
    
    
    


    
  }
  
    
  
  
  
  
}


  

int main(){
  printf("initializing navmesh statics...\n");
  
  nav_mesh* nm = newNavmesh("./mynavmesh.csv");
  Coordinate c;
  
  c = find(nm, (double)-0.0, (double)10.0);
  if (__can_walk(nm, c)){
    printf("can_walk\n");
  }else{
    printf("can't_walk");
  }
  
  return 0;
}


