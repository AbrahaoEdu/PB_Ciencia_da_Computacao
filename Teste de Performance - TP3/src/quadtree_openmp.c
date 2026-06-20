#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define SPACE 1000
#define CAPACITY 50
#define NUM_PARTICLES 100000
#define CUTOFF_DEPTH 4

typedef struct Point {
    double x, y;
} Point;

typedef struct QuadNode {
    double x_min, x_max, y_min, y_max;
    Point *points;
    int count;
    int cap;
    struct QuadNode *nw, *ne, *sw, *se;
} QuadNode;

static QuadNode *node_create(double x0, double y0, double x1, double y1) {
    QuadNode *n = calloc(1, sizeof(QuadNode));
    n->x_min = x0; n->y_min = y0; n->x_max = x1; n->y_max = y1;
    n->cap = CAPACITY;
    n->points = malloc(CAPACITY * sizeof(Point));
    return n;
}

static void node_add_point(QuadNode *n, Point p) {
    if (n->count < n->cap) {
        n->points[n->count++] = p;
        return;
    }
    if (!n->nw) {
        double mx = (n->x_min + n->x_max) / 2;
        double my = (n->y_min + n->y_max) / 2;
        n->nw = node_create(n->x_min, n->y_min, mx, my);
        n->ne = node_create(mx, n->y_min, n->x_max, my);
        n->sw = node_create(n->x_min, my, mx, n->y_max);
        n->se = node_create(mx, my, n->x_max, n->y_max);
        for (int i = 0; i < n->count; i++)
            node_add_point(
                n->points[i].x < mx ? (n->points[i].y < my ? n->nw : n->sw)
                                    : (n->points[i].y < my ? n->ne : n->se),
                n->points[i]);
        n->count = 0;
    }
    double mx = (n->x_min + n->x_max) / 2;
    double my = (n->y_min + n->y_max) / 2;
    QuadNode *child = p.x < mx ? (p.y < my ? n->nw : n->sw) : (p.y < my ? n->ne : n->se);
    node_add_point(child, p);
}

static void insert_points_seq(QuadNode *root, Point *pts, int n) {
    for (int i = 0; i < n; i++)
        node_add_point(root, pts[i]);
}

static void insert_range(QuadNode *root, Point *pts, int start, int end, int depth) {
    if (depth >= CUTOFF_DEPTH || end - start < 100) {
        for (int i = start; i < end; i++)
            node_add_point(root, pts[i]);
        return;
    }
    int mid = (start + end) / 2;
#pragma omp task shared(root, pts)
    insert_range(root, pts, start, mid, depth + 1);
#pragma omp task shared(root, pts)
    insert_range(root, pts, mid, end, depth + 1);
#pragma omp taskwait
}

static int query_radius(QuadNode *n, double qx, double qy, double r, int *found) {
    if (!n) return 0;
    double dx = fmax(n->x_min - qx, fmax(qx - n->x_max, 0));
    double dy = fmax(n->y_min - qy, fmax(qy - n->y_max, 0));
    if (dx * dx + dy * dy > r * r) return 0;
    for (int i = 0; i < n->count; i++) {
        double ddx = n->points[i].x - qx, ddy = n->points[i].y - qy;
        if (ddx * ddx + ddy * ddy <= r * r) (*found)++;
    }
    query_radius(n->nw, qx, qy, r, found);
    query_radius(n->ne, qx, qy, r, found);
    query_radius(n->sw, qx, qy, r, found);
    query_radius(n->se, qx, qy, r, found);
    return 0;
}

int main(void) {
    Point *pts = malloc(NUM_PARTICLES * sizeof(Point));
    srand(42);
    for (int i = 0; i < NUM_PARTICLES; i++) {
        pts[i].x = ((double)rand() / RAND_MAX) * SPACE;
        pts[i].y = ((double)rand() / RAND_MAX) * SPACE;
    }

    QuadNode *root = node_create(0, 0, SPACE, SPACE);
    double t0 = omp_get_wtime();
#pragma omp parallel
#pragma omp single
    insert_range(root, pts, 0, NUM_PARTICLES, 0);
    double t1 = omp_get_wtime();
    printf("Construcao quadtree: %.4fs (%d particulas)\n", t1 - t0, NUM_PARTICLES);

    double qx = 500, qy = 500, radius = 30;
    int total = 0;
    t0 = omp_get_wtime();
#pragma omp parallel for reduction(+ : total)
    for (int i = 0; i < 1000; i++) {
        int found = 0;
        query_radius(root, qx + (i % 10), qy + (i / 10), radius, &found);
        total += found;
    }
    t1 = omp_get_wtime();
    printf("Consultas paralelas (1000 queries): total vizinhos=%d tempo=%.4fs\n", total, t1 - t0);
    free(pts);
    return 0;
}
