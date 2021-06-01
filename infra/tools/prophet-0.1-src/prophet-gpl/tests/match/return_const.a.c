#include <stdio.h>

int foo(int a) {
    if (a < 0)
        return -(1 + 0);
    if (a > 100)
        return 0;
    return a * 2 + 1;
}

int main(int argc, char** argv) {
    if (argc < 2) return 0;
    int b;
    FILE *f = fopen(argv[1], "r");
    if (f == NULL) return 0;
    fscanf(f, "%d", &b);
    fclose(f);
    printf("%d\n", foo(b));
    return 0;
}
