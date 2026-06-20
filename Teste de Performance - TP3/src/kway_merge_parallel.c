#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

typedef struct {
    char **items;
    int size;
    int cap;
} StringList;

static void list_init(StringList *l) {
    l->items = NULL;
    l->size = l->cap = 0;
}

static void list_push(StringList *l, char *s) {
    if (l->size >= l->cap) {
        l->cap = l->cap ? l->cap * 2 : 64;
        l->items = realloc(l->items, l->cap * sizeof(char *));
    }
    l->items[l->size++] = s;
}

static int cmp_str(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

static StringList merge_two(StringList *a, StringList *b) {
    StringList out;
    list_init(&out);
    int i = 0, j = 0;
    while (i < a->size && j < b->size) {
        if (strcmp(a->items[i], b->items[j]) <= 0)
            list_push(&out, a->items[i++]);
        else
            list_push(&out, b->items[j++]);
    }
    while (i < a->size) list_push(&out, a->items[i++]);
    while (j < b->size) list_push(&out, b->items[j++]);
    return out;
}

static StringList merge_tree(StringList *lists, int n) {
    if (n == 1) return *lists;
    if (n == 2) return merge_two(&lists[0], &lists[1]);
    int half = n / 2;
    StringList left = merge_tree(lists, half);
    StringList right = merge_tree(lists + half, n - half);
    return merge_two(&left, &right);
}

static StringList merge_tree_parallel(StringList *lists, int n, int depth) {
    if (n <= 2 || depth <= 0)
        return merge_tree(lists, n);
    int half = n / 2;
    StringList left, right;
#pragma omp task shared(lists, half) firstprivate(depth)
    { left = merge_tree_parallel(lists, half, depth - 1); }
#pragma omp task shared(lists, half, n, depth)
    { right = merge_tree_parallel(lists + half, n - half, depth - 1); }
#pragma omp taskwait
    return merge_two(&left, &right);
}

int main(int argc, char **argv) {
    const char *path = "../../Teste de Performance - TP1/data/listagem_arquivos.txt";
    if (argc > 1) path = argv[1];

    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "Arquivo nao encontrado: %s\n", path);
        return 1;
    }

#define K 16
    StringList lists[K];
    char buf[512];
    int idx = 0;
    while (fgets(buf, sizeof(buf), f)) {
        buf[strcspn(buf, "\n")] = 0;
        if (buf[0] == 0) continue;
        list_push(&lists[idx % K], strdup(buf));
        idx++;
    }
    fclose(f);

    for (int i = 0; i < K; i++)
        qsort(lists[i].items, lists[i].size, sizeof(char *), cmp_str);

    double t0 = omp_get_wtime();
    StringList result;
#pragma omp parallel
#pragma omp single
    { result = merge_tree_parallel(lists, K, 3); }
    double t1 = omp_get_wtime();

    printf("k-way merge: %d listas -> %d itens em %.4fs\n", K, result.size, t1 - t0);
    if (result.size > 0)
        printf("Primeiro: %s | Ultimo: %s\n", result.items[0], result.items[result.size - 1]);
    return 0;
}
