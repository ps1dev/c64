/* The BYTE magazine sieve, as a workload for the C64 core. Strings are lower
   case so cc65's charmap puts them where the C64's upper-case set shows
   capitals. */
#include <stdio.h>
#include <string.h>

#define SIZE 8191
static unsigned char flags[SIZE + 1];

int main(void) {
    unsigned i, k, prime, count, iter;
    printf("sieve\n");
    for (iter = 1; iter <= 6; iter++) {
        count = 0;
        memset(flags, 1, sizeof(flags));
        for (i = 0; i <= SIZE; i++) {
            if (flags[i]) {
                prime = i + i + 3;
                for (k = i + prime; k <= SIZE; k += prime) flags[k] = 0;
                count++;
                if ((count & 63) == 0) printf("%u ", prime);
            }
        }
        printf("\npass %u: %u primes\n", iter, count);
    }
    printf("done\n");
    for (;;) {
    }
}
