#include  <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


/*simple Coordinate structure*/
typedef struct{
  int x;
  int y;
}Coordinate;

/*an abstract obstacle node, as y_coord it starts, y_coord it ends*/ 
typedef struct{
  int coll_start;
  int coll_end;
  struct y_obstacle* next;
}y_obstacle;

/*adds an obstacle to the linked list*/
y_obstacle* __append_obstacle(y_obstacle* obs, int start, int end){
  y_obstacle* new_node = NULL;
  new_node = (y_obstacle*) malloc(sizeof(y_obstacle));
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

/*frees the memory used by an y_obstacle linked list*/
void __del_obstacle(y_obstacle* head){
  y_obstacle* next;
  if (head==NULL){
    return;
  }
  next = (y_obstacle*) head->next;
  free(head);
  return __del_obstacle(next);
}

/*contains the info of a y coordinate in the mesh (start, end, obstacles)*/
typedef struct {
  int start;
  y_obstacle* obstacles;
  int end;
} abc_y;

/*an abstract navmesh*/
typedef struct {
  int x_lines;
  int y_lines;
  double* x_coords;
  double* y_coords;
  abc_y* boundings;
} nav_mesh;

typedef struct {
  double x;
  double y;
} world_coordinates;


world_coordinates get_world_coordinates(nav_mesh* nm, Coordinate coor){
  world_coordinates = wc;
  wc.x = nm->x_coords[coor.x];
  wc.y = nm->y_coords[coor.y];
  return wc;
}


/*frees the memory used by a navmesh*/
void del_navmesh(nav_mesh* nm){
  free(nm->x_coords);
  free(nm->y_coords);
  for(int i=0; i<nm->x_lines; i++){
    __del_obstacle(nm->boundings[i].obstacles);
  }
  free(nm->boundings);
  free(nm);
  return;
}

/*loads the info of a navmesh from a file to given navmesh pointer*/
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

/*returns a pointer to a new navmesh loading data from given file*/
nav_mesh* newNavmesh(char* filename){
  nav_mesh* nm = (nav_mesh*) malloc(sizeof(nav_mesh));
  __loadFromFile(nm, filename);
  return nm;
}

/*finds the closest point in the grid with given coordinates*/
Coordinate find(nav_mesh*nm, double x, double y){
  Coordinate c;
  int i = 0;
  while (nm->x_coords[i] < x &&  i<nm->x_lines){
    i++;
  }
  c.x = i;
  i = 0;
  while (nm->y_coords[i] < y && i<nm->y_lines){
    i++;
  }
  c.y = i;
  return c;
}

/*a position in worlds x,y coordinates*/
typedef struct {
  double x;
  double y;
} Position;

/*returns the position of a Coordinate in world space*/
Position from_coordinate(nav_mesh* nm, Coordinate coord){
  Position pos;
  pos.x = nm->x_coords[coord.x];
  pos.y = nm->y_coords[coord.y];
  return pos;
}

/*returns true if a given coordinate is walkable in the pointed navmesh*/
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


/*a closed node linked list*/
typedef struct{
  Coordinate coord;
  double f_score;
  Coordinate path;
  struct closed_node* next;
}closed_node;

/*a open node linked list*/
typedef struct{
  Coordinate coord;
  Coordinate path;
  double h_score;
  double f_score;
  struct open_node* next;
}open_node;

/*creates a closed_closed node*/
closed_node* create_closed_node(open_node* from_open){
  closed_node* new_node;

  new_node = (closed_node*) malloc(sizeof(closed_node));
  new_node->coord = from_open->coord;
  new_node->path = from_open->path;
  new_node->f_score = from_open->f_score;
  new_node->next = NULL;

  return new_node;

}

/*appends a open_node in the list according to it's f_score value*/
open_node* sorted_append(open_node* list, open_node* new_node){
  if (list == NULL){
    return new_node;
  }
  
  if (list->h_score >= new_node->h_score){
    new_node->next = (struct open_node*)list;
    return new_node;
  }
  
  open_node* current = (open_node*)list->next;
  open_node* last = list;
  
  
  while(current!=NULL){
    if (current->h_score >= new_node->h_score){
      last->next = (struct open_node*) new_node;
      new_node->next = (struct open_node*) current;
      return list;
    }
    last = current;
    current = (open_node*) current->next;
  }
  last->next = (struct open_node*)new_node;
  return list;
}

/*the function extimating the distance from target node (simple distance between points)*/
double h_func(Coordinate current, Coordinate end){
  return sqrt(pow(end.x-current.x, 2) + pow(end.y-current.y, 2));
}

/*creates an open node*/
open_node* create_open_node(Coordinate coord, Coordinate end, Coordinate path, double f_score){
  open_node* new_node = (open_node*) malloc(sizeof(open_node));
  new_node->coord = coord;
  new_node->path = path;
  new_node->h_score = h_func(coord, end);
  new_node->f_score = f_score;
  new_node->next = NULL;
  return new_node;
}

/*returns the pointer of a closed_node in a list if present, NULL otherwise*/
closed_node* get_from_closed(closed_node* list, Coordinate coord){
  while(list!=NULL){
    if (list->coord.x == coord.x && list->coord.y == coord.y){
      return list;
    }
    list = (closed_node*) list->next;
  }
  return NULL;
}

/*returns the pointer of a open_node in a list if present, NULL otherwise*/
open_node* get_from_open(open_node* list, Coordinate coord){
  while(list!=NULL){
    if (list->coord.x == coord.x && list->coord.x == coord.y){
      return list;
    }
    list = (open_node*) list->next;
  }
  return NULL;
}

/*free the memory occupied by a open_node list*/
//TODO: tail recursion
void free_open(open_node* list){
  if (list!=NULL){
    free_open((open_node*) list->next);
    free(list);
    return;
  }
  return;
}

/*a path node for a linked list*/
typedef struct{
  Coordinate coord;
  struct path_node* next;
}path_node;

/*frees the memory for a allocated path_node*/
void free_path(path_node* node){
  if (node!=NULL){
    free_path((path_node*)node->next);
    }
  free(node);
  return;
}

/*creates a new path_node with given info*/
path_node* new_path_node(Coordinate coord){
  path_node* new_node = NULL;
  new_node = malloc(sizeof(path_node));
  new_node->coord = coord;
  new_node->next = NULL;
  return new_node; 
}

/*pops a closed_node from a list from a closed_node list pointer*/
closed_node* pop_closed(closed_node** list, Coordinate coord){
  closed_node* last;
  closed_node* current;
  if (*list == NULL){
    return NULL;
  }

  if ((*list)->coord.x == coord.x && (*list)->coord.y == coord.y){
    current = *list;
    (*list) = (closed_node*)(*list)->next;
    return current;
  }
  
  last = *list;
  current = (closed_node*) last->next;
  
  while (current != NULL){
    if (current->coord.x == coord.x && current->coord.y == coord.y){
      last->next = current->next;
      return current;
    }
    last = current;
    current = (closed_node*)current->next;
  }
  return NULL;
}

/*frees the memory occupied by a closed_node list*/
//TODO: tail recursion
void free_closed_set(closed_node* list){
  if (list != NULL){
    free_closed_set((closed_node*)list->next);
  }
  free(list);
}

//DEBUG
/*prints a closed set*/
void print_closed_set(closed_node* list){
  while (list != NULL){
    printf("(%d,%d)-(%d,%d)\n", list->coord.x, list->coord.y, list->path.x, list->path.y);
    list = (closed_node*) list->next;
  }
  return;
}

/*returns a path from a closed_node list pointer, a start and an end Coordinate*/
path_node* reconstruct_path(Coordinate start, Coordinate end, closed_node** closed_set){
  closed_node* current;
  path_node* path = NULL;
  path_node* path_node;
  Coordinate next_coord = end;
  
  while (next_coord.x != start.x || next_coord.y != start.y){
    path_node = new_path_node(next_coord);
    path_node->next = (struct path_node*)path;
    path = path_node;
    
    current = pop_closed(closed_set, next_coord);
    next_coord = current->path;
    free(current);
  }
  
  return path;
 
}


#define SQRT2 1.4142

/*A* algorythm, returns a path walkable in the navmesh*/
//TODO: resort open_set list when finding a better path

path_node* a_star(nav_mesh* nm, Coordinate start, Coordinate end){
  Coordinate neighbors[8];
  neighbors[0].x = -1;
  neighbors[0].y = -1;
  open_node* open_set = create_open_node(start, end, neighbors[0], (double)0.0);
  closed_node* closed_set = NULL;
  open_node* current = NULL;
  closed_node* found_closed;
  open_node* found_open;
  path_node* path = NULL;

  /*helper function called for each neighbor Coordinate*/
  void explore_neighbor(Coordinate _coor, double dist){
    if (__can_walk(nm, _coor)){
      found_closed = get_from_closed(closed_set, _coor);
      if (found_closed!=NULL){
	if(found_closed->f_score > current->f_score+dist){
	  found_closed->f_score = current->f_score+dist;
	  found_closed->path = current->coord;
	}
      }else{
	found_open = get_from_open(open_set, _coor);
	if (found_open!=NULL){
	  if (found_open->f_score > current->f_score + dist){
	    found_open->f_score = current->f_score + dist;
	    found_open->path = current->coord;
	  }
	}else{
	  open_set = sorted_append(open_set, create_open_node(_coor, end,current->coord, current->f_score+dist));
	}
      }
    }
  }
  
  while(open_set != NULL){
    current = open_set;
    open_set = (open_node*) open_set->next;
    
    if (current->coord.x == end.x && current->coord.y == end.y){
      found_closed = create_closed_node(current);
      found_closed->next = (struct closed_node*)closed_set;
      closed_set = found_closed;
      print_closed_set(closed_set);
      free_open(open_set);
      path = reconstruct_path(start, end, &closed_set);
      free_closed_set(closed_set);
      return path;
    }
    

    neighbors[0].x = current->coord.x-1;
    neighbors[0].y = current->coord.y-1;
    
    neighbors[1].x = current->coord.x+1;
    neighbors[1].y = current->coord.y-1;
    
    neighbors[2].x = current->coord.x+1;
    neighbors[2].y = current->coord.y+1;

    neighbors[3].x = current->coord.x-1;
    neighbors[3].y = current->coord.y+1;

    neighbors[4].x = current->coord.x;
    neighbors[4].y = current->coord.y-1;

    neighbors[5].x = current->coord.x;
    neighbors[5].y = current->coord.y+1;

    neighbors[6].x = current->coord.x-1;
    neighbors[6].y = current->coord.y;

    neighbors[7].x = current->coord.x+1;
    neighbors[7].y = current->coord.y;


    for (int i=0; i<4; i++){
      explore_neighbor(neighbors[i], SQRT2);
    }
    for (int i=4; i<8; i++){
      explore_neighbor(neighbors[i], 1.0);
    }
    found_closed = create_closed_node(current);
    found_closed->next = (struct closed_node*)closed_set;
    closed_set = found_closed;
    free(current);
  }
  free_closed_set(closed_set);
  printf("no path founded\n");
  return NULL;
}

/*returns the path between two given points*/
path_node* find_path(nav_mesh* nm, double start_x, double start_y, double end_x, double end_y){
  Coordinate start, end;
  path_node* path = NULL;
  start = find(nm, start_x, start_y);
  end = find(nm, end_x, end_y);
  
  if (!__can_walk(nm, start)||!__can_walk(nm, end)){
    printf("path not found A\n");
    return NULL;
  }
  
  path = a_star(nm, start, end);
  path_node* tmp = path;
  
  while(tmp!=NULL){
    printf("(%d,%d) -> ", tmp->coord.x, tmp->coord.y);
    tmp = (path_node*)tmp-> next;
  }
  printf("\n");
  
  return path;
}





void main(){
  printf("initializing navmesh statics...\n");
  
  nav_mesh* nm = newNavmesh("./mynavmesh.csv");
  Coordinate c1, c2;
  
  c1 = find(nm, (double)0.4, (double)0.3);
  if (__can_walk(nm, c1)){
    printf("can_walk\n");
  }else{
    printf("can't_walk\n");
  }
  
  c2 = find(nm, (double)0.5, (double)0.3);
  if (__can_walk(nm, c2)){
    printf("can_walk\n");
  }else{
    printf("can't_walk\n");
  }
  printf("#################################\n");
  printf("searching path.....\n");
  
  a_star(nm, c1, c2);
  
  return ;
}

