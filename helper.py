#!/usr/bin/env python3
"""
helper.py -- Offline CLI study helper tool.

Usage:
  python helper.py list
  python helper.py list <subject>
  python helper.py show  <subject> <topic_num>
  python helper.py write <subject> <topic_num> [filename]
  python helper.py copy  <subject> <topic_num>

For AOA experiments, you can specify '1', 'exp1', or 'exp 1'.
"""

import sys
import os
import re
import subprocess

# -----------------------------------------------------------------------------
#  DATA -- Edit titles, notes, and code blocks here.
#  Each topic has:
#    title : short display name
#    notes : plain-text explanation / steps
#    code  : paste your code snippet between the triple-quotes
# -----------------------------------------------------------------------------

SUBJECTS = {
    "aoa": {
        "1": {
            "title": "Exp 01: Insertion Sort and Selection Sort",
            "notes": "",
            "code": r"""
#include <stdio.h>

void insertionSort(int a[], int n)
{
    int i, j, key;

    for (i = 1; i < n; i++)
    {
        key = a[i];
        j = i - 1;

        while (j >= 0 && a[j] > key)
        {
            a[j + 1] = a[j];
            j--;
        }

        a[j + 1] = key;
    }
}

void selectionSort(int a[], int n)
{
    int i, j, min, temp;

    for (i = 0; i < n - 1; i++)
    {
        min = i;

        for (j = i + 1; j < n; j++)
        {
            if (a[j] < a[min])
            {
                min = j;
            }
        }

        temp = a[i];
        a[i] = a[min];
        a[min] = temp;
    }
}

int main()
{
    int n, choice, i;
    int a[50];

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter %d integers: ", n);
    for (i = 0; i < n; i++)
    {
        scanf("%d", &a[i]);
    }

    printf("Choose (1 for Insertion Sort, 2 for Selection Sort): ");
    scanf("%d", &choice);

    if (choice == 1)
    {
        insertionSort(a, n);
    }
    else
    {
        selectionSort(a, n);
    }

    printf("Sorted array: ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", a[i]);
    }
    printf("\n");

    return 0;
}
""",
        },
        "2": {
            "title": "Exp 02: Binary Search using Divide and Conquer",
            "notes": "",
            "code": r"""
#include <stdio.h>

int binarySearch(int a[], int low, int high, int key)
{
    int mid;

    if (low > high)
    {
        return -1;
    }

    mid = (low + high) / 2;

    if (a[mid] == key)
    {
        return mid;
    }
    else if (a[mid] > key)
    {
        return binarySearch(a, low, mid - 1, key);
    }
    else
    {
        return binarySearch(a, mid + 1, high, key);
    }
}

int main()
{
    int n, i, key, pos;
    int a[50];

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter %d sorted elements: ", n);
    for (i = 0; i < n; i++)
    {
        scanf("%d", &a[i]);
    }

    printf("Enter element to search: ");
    scanf("%d", &key);

    pos = binarySearch(a, 0, n - 1, key);

    if (pos != -1)
    {
        printf("Success: %d found at index %d (position %d).\n", key, pos, pos + 1);
    }
    else
    {
        printf("Element %d not found in the array.\n", key);
    }

    return 0;
}
""",
        },
        "3": {
            "title": "Exp 03: Quick Sort using Divide and Conquer",
            "notes": "",
            "code": r"""
#include <stdio.h>

void swap(int *a, int *b)
{
    int temp;

    temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int a[], int low, int high)
{
    int pivot, i, j;

    pivot = a[high];
    i = low - 1;

    for (j = low; j < high; j++)
    {
        if (a[j] < pivot)
        {
            i++;
            swap(&a[i], &a[j]);
        }
    }

    swap(&a[i + 1], &a[high]);

    return i + 1;
}

void quickSort(int a[], int low, int high)
{
    int pivot;

    if (low < high)
    {
        pivot = partition(a, low, high);
        quickSort(a, low, pivot - 1);
        quickSort(a, pivot + 1, high);
    }
}

int main()
{
    int n, i;
    int a[50];

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
    {
        scanf("%d", &a[i]);
    }

    quickSort(a, 0, n - 1);

    printf("Sorted array (Quick Sort): ");
    for (i = 0; i < n; i++)
    {
        printf("%d ", a[i]);
    }
    printf("\n");

    return 0;
}
""",
        },
        "4": {
            "title": "Exp 04: Fractional Knapsack using Greedy Method",
            "notes": "",
            "code": r"""
#include <stdio.h>

void swap(float *a, float *b)
{
    float temp;

    temp = *a;
    *a = *b;
    *b = temp;
}

int main()
{
    int n, i, j;
    float profit[20], weight[20], ratio[20];
    float capacity, total = 0;

    printf("Enter number of items: ");
    scanf("%d", &n);

    for (i = 0; i < n; i++)
    {
        printf("Item %d (Profit Weight): ", i + 1);
        scanf("%f %f", &profit[i], &weight[i]);

        ratio[i] = profit[i] / weight[i];
    }

    printf("Enter knapsack capacity: ");
    scanf("%f", &capacity);

    for (i = 0; i < n - 1; i++)
    {
        for (j = i + 1; j < n; j++)
        {
            if (ratio[i] < ratio[j])
            {
                swap(&ratio[i], &ratio[j]);
                swap(&profit[i], &profit[j]);
                swap(&weight[i], &weight[j]);
            }
        }
    }

    for (i = 0; i < n; i++)
    {
        if (weight[i] <= capacity)
        {
            total += profit[i];
            capacity -= weight[i];
        }
        else
        {
            total += profit[i] * (capacity / weight[i]);
            break;
        }
    }

    printf("Maximum Profit = %.2f\n", total);

    return 0;
}
""",
        },
        "5": {
            "title": "Exp 05: Prim's Minimum Spanning Tree (MST) Algorithm",
            "notes": "",
            "code": r"""
#include <stdio.h>
#define INF 9999

int main()
{
    int n, i, j, k;
    int cost[20][20];
    int visited[20] = {0};
    int total = 0;
    int min, u, v;

    printf("Enter number of vertices: ");
    scanf("%d", &n);

    printf("Enter cost matrix (use 0 for self/no edge):\n");
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            scanf("%d", &cost[i][j]);

            if (cost[i][j] == 0)
            {
                cost[i][j] = INF;
            }
        }
    }

    visited[0] = 1;
    printf("\nSelected MST Edges:\n");

    for (k = 0; k < n - 1; k++)
    {
        min = INF;
        u = 0;
        v = 0;

        for (i = 0; i < n; i++)
        {
            if (visited[i])
            {
                for (j = 0; j < n; j++)
                {
                    if (!visited[j] && cost[i][j] < min)
                    {
                        min = cost[i][j];
                        u = i;
                        v = j;
                    }
                }
            }
        }

        visited[v] = 1;
        printf("Edge %d: (%d -> %d) with Cost = %d\n", k + 1, u, v, min);
        total += min;
    }

    printf("Total MST Cost = %d\n", total);

    return 0;
}
""",
        },
        "6": {
            "title": "Exp 06: All-Pairs Shortest Path (Floyd-Warshall)",
            "notes": "",
            "code": r"""
#include <stdio.h>
#define INF 999

int main()
{
    int n, i, j, k;
    int dist[20][20];

    printf("Enter number of vertices: ");
    scanf("%d", &n);

    printf("Enter weighted matrix (use 999 for INF):\n");
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            scanf("%d", &dist[i][j]);
        }
    }

    for (k = 0; k < n; k++)
    {
        for (i = 0; i < n; i++)
        {
            for (j = 0; j < n; j++)
            {
                if (dist[i][k] + dist[k][j] < dist[i][j])
                {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }

    printf("\nAll-Pairs Shortest Distance Matrix:\n");
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            if (dist[i][j] >= INF)
            {
                printf("INF\t");
            }
            else
            {
                printf("%d\t", dist[i][j]);
            }
        }
        printf("\n");
    }

    return 0;
}
""",
        },
        "7": {
            "title": "Exp 07: Sum of Subset using Backtracking",
            "notes": "",
            "code": r"""
#include <stdio.h>

int set[20], chosen[20];
int n, target, found = 0;

void findSubsets(int index, int sum)
{
    int i;

    if (sum == target)
    {
        found = 1;
        printf("{ ");

        for (i = 0; i < index; i++)
        {
            if (chosen[i])
            {
                printf("%d ", set[i]);
            }
        }

        printf("}\n");
        return;
    }

    if (index == n || sum > target)
    {
        return;
    }

    chosen[index] = 1;
    findSubsets(index + 1, sum + set[index]);

    chosen[index] = 0;
    findSubsets(index + 1, sum);
}

int main()
{
    int i;

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter %d positive integers: ", n);
    for (i = 0; i < n; i++)
    {
        scanf("%d", &set[i]);
    }

    printf("Enter target sum: ");
    scanf("%d", &target);

    printf("\nSubsets summing to %d:\n", target);
    findSubsets(0, 0);

    if (!found)
    {
        printf("No subset found with target sum.\n");
    }

    return 0;
}
""",
        },
        "8": {
            "title": "Exp 08: N-Queens Problem using Backtracking",
            "notes": "",
            "code": r"""
#include <stdio.h>
#include <stdlib.h>

int board[20];
int n;

int isSafe(int row, int col)
{
    int i;

    for (i = 0; i < row; i++)
    {
        if (board[i] == col || abs(board[i] - col) == abs(i - row))
        {
            return 0;
        }
    }

    return 1;
}

int solve(int row)
{
    int col;

    if (row == n)
    {
        return 1;
    }

    for (col = 0; col < n; col++)
    {
        if (isSafe(row, col))
        {
            board[row] = col;

            if (solve(row + 1))
            {
                return 1;
            }
        }
    }

    return 0;
}

int main()
{
    int i, j;

    printf("Enter number of Queens (N): ");
    scanf("%d", &n);

    if (solve(0))
    {
        printf("\nSolution board placement:\n");

        for (i = 0; i < n; i++)
        {
            for (j = 0; j < n; j++)
            {
                if (board[i] == j)
                {
                    printf("Q ");
                }
                else
                {
                    printf(". ");
                }
            }
            printf("\n");
        }
    }
    else
    {
        printf("No valid placement exists for N = %d.\n", n);
    }

    return 0;
}
""",
        },
        "9": {
            "title": "Exp 09: Rabin-Karp String Matching Algorithm",
            "notes": "",
            "code": r"""
#include <stdio.h>
#include <string.h>

#define D 256
#define Q 101

int main()
{
    char text[100], pattern[50];
    int n, m, i, j;
    int patternHash = 0, textHash = 0, h = 1;
    int found = 0;

    printf("Enter text string (no spaces): ");
    scanf("%s", text);

    printf("Enter pattern to search: ");
    scanf("%s", pattern);

    n = strlen(text);
    m = strlen(pattern);

    for (i = 0; i < m - 1; i++)
    {
        h = (h * D) % Q;
    }

    for (i = 0; i < m; i++)
    {
        patternHash = (D * patternHash + pattern[i]) % Q;
        textHash = (D * textHash + text[i]) % Q;
    }

    for (i = 0; i <= n - m; i++)
    {
        if (patternHash == textHash)
        {
            for (j = 0; j < m; j++)
            {
                if (text[i + j] != pattern[j])
                {
                    break;
                }
            }

            if (j == m)
            {
                printf("Pattern found at index %d\n", i);
                found = 1;
            }
        }

        if (i < n - m)
        {
            textHash = (D * (textHash - text[i] * h) + text[i + m]) % Q;

            if (textHash < 0)
            {
                textHash += Q;
            }
        }
    }

    if (!found)
    {
        printf("Pattern not found in text.\n");
    }

    return 0;
}
""",
        },
        "10": {
            "title": "Exp 10: Min-Max Algorithm using Divide and Conquer",
            "notes": "",
            "code": r"""
#include <stdio.h>

void findMinMax(int a[], int low, int high, int *min, int *max)
{
    int mid;
    int leftMin, leftMax, rightMin, rightMax;

    if (low == high)
    {
        *min = a[low];
        *max = a[low];
        return;
    }

    if (high == low + 1)
    {
        if (a[low] < a[high])
        {
            *min = a[low];
            *max = a[high];
        }
        else
        {
            *min = a[high];
            *max = a[low];
        }
        return;
    }

    mid = (low + high) / 2;

    findMinMax(a, low, mid, &leftMin, &leftMax);
    findMinMax(a, mid + 1, high, &rightMin, &rightMax);

    if (leftMin < rightMin)
    {
        *min = leftMin;
    }
    else
    {
        *min = rightMin;
    }

    if (leftMax > rightMax)
    {
        *max = leftMax;
    }
    else
    {
        *max = rightMax;
    }
}

int main()
{
    int n, i, min, max;
    int a[50];

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
    {
        scanf("%d", &a[i]);
    }

    findMinMax(a, 0, n - 1, &min, &max);

    printf("Minimum element = %d\n", min);
    printf("Maximum element = %d\n", max);

    return 0;
}
""",
        },
    },

    "coa": {
        "1": {
            "title": "Exp 01: Decimal and Hexadecimal to Binary Conversion",
            "notes": "Aim: Convert a decimal number and a hexadecimal number into binary. | Category: Number System Conversion",
            "code": r"""
#include <stdio.h>
#include <ctype.h>

void decimalToBinary(int n)
{
    int bits[32], idx = 0, i;

    if (n == 0)
    {
        printf("0\n");
        return;
    }

    while (n > 0)
    {
        bits[idx] = n % 2;
        idx++;
        n /= 2;
    }

    for (i = idx - 1; i >= 0; i--)
    {
        printf("%d", bits[i]);
    }

    printf("\n");
}

void hexToBinary(char hex[])
{
    int i, b, val;
    char c;

    for (i = 0; hex[i] != '\0'; i++)
    {
        c = toupper(hex[i]);
        val = (c >= '0' && c <= '9') ? (c - '0') : (c - 'A' + 10);

        for (b = 3; b >= 0; b--)
        {
            printf("%d", (val >> b) & 1);
        }
    }

    printf("\n");
}

int main()
{
    int dec;
    char hex[20];

    printf("Enter a Decimal number: ");
    scanf("%d", &dec);

    printf("Binary of Decimal %d = ", dec);
    decimalToBinary(dec);

    printf("\nEnter a Hexadecimal number: ");
    scanf("%s", hex);

    printf("Binary of Hexadecimal %s = ", hex);
    hexToBinary(hex);

    return 0;
}
""",
        },
        "2": {
            "title": "Exp 02: 2's Complement of a Binary Number",
            "notes": "Aim: Find the 2's complement of a binary number. | Category: Signed Binary Representation",
            "code": r"""
#include <stdio.h>
#include <string.h>

int main()
{
    char binary[100];
    int i, len;

    printf("Enter a binary number: ");
    scanf("%s", binary);

    len = strlen(binary);

    for (i = len - 1; i >= 0; i--)
    {
        if (binary[i] == '1')
        {
            break;
        }
    }

    if (i == -1)
    {
        printf("2's Complement: 1%s\n", binary);
    }
    else
    {
        for (i = i - 1; i >= 0; i--)
        {
            if (binary[i] == '1')
            {
                binary[i] = '0';
            }
            else
            {
                binary[i] = '1';
            }
        }

        printf("2's Complement: %s\n", binary);
    }

    return 0;
}
""",
        },
        "3": {
            "title": "Exp 03: Basic Arithmetic Operations on 8-Bit Data",
            "notes": "Aim: Perform addition, subtraction, multiplication, and division on 8-bit data. | Category: ALU Arithmetic Operations",
            "code": r"""
.MODEL SMALL
.DATA
    NUM1 DB 14H
    NUM2 DB 06H
    SUM  DB ?
    DIFF DB ?
    PROD DW ?
    QUOT DB ?
    REM  DB ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV AL, NUM1
    ADD AL, NUM2
    MOV SUM, AL
    MOV AL, NUM1
    SUB AL, NUM2
    MOV DIFF, AL
    MOV AL, NUM1
    MOV BL, NUM2
    MUL BL
    MOV PROD, AX
    MOV AX, 0000H
    MOV AL, NUM1
    DIV BL
    MOV QUOT, AL
    MOV REM, AH
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
""",
            "code_type": "asm",
        },
        "4": {
            "title": "Exp 04: Basic Logical Operations (AND, OR, XOR, NOT) on 8-Bit Data",
            "notes": "Aim: Perform AND, OR, XOR, and NOT on 8-bit data. | Category: ALU Logical Operations",
            "code": r"""
.MODEL SMALL
.DATA
    OP1     DB 92H
    OP2     DB 6AH
    RES_AND DB ?
    RES_OR  DB ?
    RES_XOR DB ?
    RES_NOT DB ?
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV AL, OP1
    AND AL, OP2
    MOV RES_AND, AL
    MOV AL, OP1
    OR  AL, OP2
    MOV RES_OR, AL
    MOV AL, OP1
    XOR AL, OP2
    MOV RES_XOR, AL
    MOV AL, OP1
    NOT AL
    MOV RES_NOT, AL
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
""",
            "code_type": "asm",
        },
        "5": {
            "title": "Exp 05: Signed 8-Bit Multiplication using Booth's Algorithm",
            "notes": "Aim: Multiply two signed 8-bit numbers using Booth's Algorithm. | Category: Signed Multiplication Algorithm",
            "code": r"""
#include <stdio.h>

int main()
{
    int M, Q, A = 0, Q_1 = 0, n = 8;
    int step, Q0, signA, product;

    printf("Enter signed Multiplicand (M): ");
    scanf("%d", &M);

    printf("Enter signed Multiplier (Q): ");
    scanf("%d", &Q);

    M &= 0xFF;
    Q &= 0xFF;

    for (step = 1; step <= n; step++)
    {
        Q0 = Q & 1;

        if (Q0 == 0 && Q_1 == 1)
        {
            A = (A + M) & 0xFF;
        }
        else if (Q0 == 1 && Q_1 == 0)
        {
            A = (A - M) & 0xFF;
        }

        signA = A & 0x80;
        Q_1 = Q & 1;
        Q = (Q >> 1) | ((A & 1) << 7);
        A = (A >> 1) | signA;
    }

    product = (A << 8) | Q;

    if (product & 0x8000)
    {
        product -= 0x10000;
    }

    printf("Final 16-bit Register [A:Q] = 0x%04X\n", (A << 8) | Q);
    printf("Signed Product = %d\n", product);

    return 0;
}
""",
        },
        "6": {
            "title": "Exp 06: Unsigned 8-Bit Division using Restoring Division Algorithm",
            "notes": "Aim: Divide two unsigned 8-bit numbers using the Restoring Division Algorithm. | Category: Unsigned Division Algorithm",
            "code": r"""
#include <stdio.h>

int main()
{
    int Q, M;
    int A = 0;
    int n = 8;
    int i;

    printf("Enter Dividend (Q): ");
    scanf("%d", &Q);

    printf("Enter Divisor (M): ");
    scanf("%d", &M);

    if (M == 0)
    {
        printf("Error: Division by zero is not allowed.\n");
        return 0;
    }

    for (i = 0; i < n; i++)
    {
        A = (A << 1) | ((Q >> (n - 1)) & 1);
        Q = (Q << 1) & 0xFF;

        A = A - M;

        if (A < 0)
        {
            A = A + M;
        }
        else
        {
            Q = Q | 1;
        }
    }

    printf("\nQuotient = %d\n", Q);
    printf("Remainder = %d\n", A);

    return 0;
}
""",
        },
        "7": {
            "title": "Exp 07: Direct Mapping Technique of Cache Memory",
            "notes": "Aim: Simulate the Direct Mapping Technique of cache memory. | Category: Cache Memory Organization",
            "code": r"""
#include <stdio.h>

int main()
{
    int numLines, numReq, cache[32];
    int hits = 0, misses = 0;
    int i, block, line;

    printf("Enter number of Cache Lines: ");
    scanf("%d", &numLines);

    for (i = 0; i < numLines; i++)
    {
        cache[i] = -1;
    }

    printf("Enter number of Memory Block requests: ");
    scanf("%d", &numReq);

    printf("Enter %d Memory Block numbers: ", numReq);
    for (i = 0; i < numReq; i++)
    {
        scanf("%d", &block);
        line = block % numLines;

        if (cache[line] == block)
        {
            hits++;
            printf("Access Block %d -> Line %d : CACHE HIT\n", block, line);
        }
        else
        {
            misses++;
            cache[line] = block;
            printf("Access Block %d -> Line %d : CACHE MISS (Loaded Block %d)\n", block, line, block);
        }
    }

    printf("\nFinal Cache Table:\n");
    for (i = 0; i < numLines; i++)
    {
        if (cache[i] != -1)
        {
            printf("Line %d : Block %d\n", i, cache[i]);
        }
        else
        {
            printf("Line %d : Empty\n", i);
        }
    }

    printf("Total Hits = %d | Total Misses = %d\n", hits, misses);

    return 0;
}
""",
        },
        "8": {
            "title": "Exp 08: Sorting an Array of 8-Bit Numbers in Ascending Order",
            "notes": "Aim: Sort an array of 8-bit numbers in ascending order using Bubble Sort. | Category: Data Manipulation / Sorting",
            "code": r"""
.MODEL SMALL
.DATA
    ARRAY DB 45H, 12H, 78H, 34H
    COUNT EQU 4
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV CX, COUNT - 1
OUTER:
    MOV DX, CX
    LEA SI, ARRAY
INNER:
    MOV AL, [SI]
    CMP AL, [SI + 1]
    JBE NO_SWAP
    XCHG AL, [SI + 1]
    MOV [SI], AL
NO_SWAP:
    INC SI
    DEC DX
    JNZ INNER
    LOOP OUTER
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
""",
            "code_type": "asm",
        },
        "9": {
            "title": "Exp 09: Block Transfer using Index Registers (SI and DI)",
            "notes": "Aim: Transfer a block of data using the SI and DI index registers. | Category: Memory Block Transfer",
            "code": r"""
.MODEL SMALL
.DATA
    SRC_BLK  DB 10H, 20H, 30H, 40H, 50H
    DEST_BLK DB 5 DUP(0)
    COUNT    EQU 5
.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX
    MOV ES, AX
    LEA SI, SRC_BLK
    LEA DI, DEST_BLK
    MOV CX, COUNT
    CLD
    REP MOVSB
    MOV AH, 4CH
    INT 21H
MAIN ENDP
END MAIN
""",
            "code_type": "asm",
        },
        "10": {
            "title": "Exp 10: Basic File Operations in C (Create, Write, Append, Read)",
            "notes": "Aim: Create, write, append, and read a file using user input. | Category: Secondary Storage / File I/O",
            "code": r"""
#include <stdio.h>

int main()
{
    FILE *fp;
    char line1[100], line2[100], buffer[100];

    printf("Enter initial line to write to file: ");
    fgets(line1, sizeof(line1), stdin);

    fp = fopen("coa_record.txt", "w");
    fprintf(fp, "%s", line1);
    fclose(fp);

    printf("Enter second line to append to file: ");
    fgets(line2, sizeof(line2), stdin);

    fp = fopen("coa_record.txt", "a");
    fprintf(fp, "%s", line2);
    fclose(fp);

    printf("\n--- Contents Read from coa_record.txt ---\n");
    fp = fopen("coa_record.txt", "r");
    while (fgets(buffer, sizeof(buffer), fp) != NULL)
    {
        printf("%s", buffer);
    }
    fclose(fp);

    return 0;
}
""",
        },
    },

    "subject3": {
        "1": {
            "title": "Topic 1 Title",
            "notes": "Core logic and steps for subject3 topic 1.",
            "code": """\
""",
        },
        "2": {
            "title": "Topic 2 Title",
            "notes": "Core logic and steps for subject3 topic 2.",
            "code": """\
""",
        },
        "3": {
            "title": "Topic 3 Title",
            "notes": "Core logic and steps for subject3 topic 3.",
            "code": """\
""",
        },
        "4": {
            "title": "Topic 4 Title",
            "notes": "Core logic and steps for subject3 topic 4.",
            "code": """\
""",
        },
        "5": {
            "title": "Topic 5 Title",
            "notes": "Core logic and steps for subject3 topic 5.",
            "code": """\
""",
        },
        "6": {
            "title": "Topic 6 Title",
            "notes": "Core logic and steps for subject3 topic 6.",
            "code": """\
""",
        },
        "7": {
            "title": "Topic 7 Title",
            "notes": "Core logic and steps for subject3 topic 7.",
            "code": """\
""",
        },
        "8": {
            "title": "Topic 8 Title",
            "notes": "Core logic and steps for subject3 topic 8.",
            "code": """\
""",
        },
        "9": {
            "title": "Topic 9 Title",
            "notes": "Core logic and steps for subject3 topic 9.",
            "code": """\
""",
        },
        "10": {
            "title": "Topic 10 Title",
            "notes": "Core logic and steps for subject3 topic 10.",
            "code": """\
""",
        },
    },
}

# -----------------------------------------------------------------------------
#  HELPERS
# -----------------------------------------------------------------------------

DIVIDER = "=" * 60


def _valid_subjects():
    return sorted(SUBJECTS.keys())


def _valid_topics(subject):
    s = _resolve_subject(subject)
    if not s or s not in SUBJECTS:
        return []
    keys = [k for k in SUBJECTS[s].keys() if k.isdigit()]
    return sorted(keys, key=int)


def _resolve_subject(raw):
    """Return the canonical subject key or None."""
    if not raw:
        return None
    raw_str = str(raw).strip().lower()
    for s in SUBJECTS:
        if s.lower() == raw_str:
            return s
    # Backward-compatible alias for subject1
    if raw_str in ("subject1", "sub1", "s1"):
        if "aoa" in SUBJECTS:
            return "aoa"
    # Backward-compatible alias for subject2
    if raw_str in ("subject2", "sub2", "s2"):
        if "coa" in SUBJECTS:
            return "coa"
    return None


def _resolve_topic(subject, raw):
    """Return the canonical topic key or None."""
    s = _resolve_subject(subject)
    if not s or s not in SUBJECTS:
        return None
    topics = SUBJECTS[s]
    raw_str = str(raw).strip().lower()

    if raw_str in topics:
        return raw_str

    # Normalize variations: 'exp1', 'exp01', 'exp 1', 'experiment 1', 'topic 1'
    cleaned = re.sub(r"^(exp|experiment|topic)[\s_\-]*", "", raw_str)
    if cleaned in topics:
        return cleaned

    # Strip leading zeroes: '01' -> '1'
    cleaned_num = cleaned.lstrip("0") or "0"
    if cleaned_num in topics:
        return cleaned_num

    return None


def _normalize_args(args):
    """
    Handle split arguments such as:
      ['aoa', 'exp', '1'] -> ['aoa', 'exp1']
      ['aoa', 'exp', '01', 'custom.c'] -> ['aoa', 'exp01', 'custom.c']
      ['aoa', 'topic', '1'] -> ['aoa', '1']
    """
    if len(args) >= 3 and args[1].lower() in ("exp", "experiment", "topic"):
        return [args[0], f"exp{args[2]}"] + args[3:]
    return args


def _get_topic(subject, topic_num):
    """Validated lookup; prints error and exits on bad input."""
    s = _resolve_subject(subject)
    if s is None:
        print(f"[error] Unknown subject: '{subject}'")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)
    t = _resolve_topic(s, topic_num)
    if t is None:
        is_experiment = s in ("aoa", "coa")
        label = "experiment" if is_experiment else "topic"
        print(f"[error] Unknown {label} identifier: '{topic_num}' for subject '{s}'")
        valid_items = [f"exp{k}" if is_experiment else k for k in _valid_topics(s)]
        print(f"        Valid {label}s: {', '.join(valid_items)} (or 1..{len(valid_items)})")
        sys.exit(1)
    return SUBJECTS[s][t]


def _copy_to_clipboard(text):
    """Try multiple clipboard strategies; degrade gracefully."""
    platform = sys.platform
    try:
        if platform == "win32":
            proc = subprocess.Popen(
                ["clip"], stdin=subprocess.PIPE, shell=True
            )
            proc.communicate(input=text.encode("utf-16"))
            if proc.returncode == 0:
                return True
        elif platform == "darwin":
            proc = subprocess.Popen(
                ["pbcopy"], stdin=subprocess.PIPE
            )
            proc.communicate(input=text.encode("utf-8"))
            if proc.returncode == 0:
                return True
        else:  # Linux / BSD - try xclip, then xsel
            for cmd in (["xclip", "-selection", "clipboard"],
                        ["xsel", "--clipboard", "--input"]):
                try:
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    proc.communicate(input=text.encode("utf-8"))
                    if proc.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
    except Exception:
        pass

    # Strategy 2: tkinter fallback (cross-platform, part of stdlib if GUI installed)
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.after(300, root.destroy)
        root.mainloop()
        return True
    except Exception:
        pass

    return False


# -----------------------------------------------------------------------------
#  COMMANDS
# -----------------------------------------------------------------------------

def cmd_list(args):
    """
    list           -> list all subjects
    list <subject> -> list topics/experiments in that subject
    """
    if len(args) == 0:
        print(DIVIDER)
        print("  Available Subjects")
        print(DIVIDER)
        for s in _valid_subjects():
            if s == "aoa":
                print(f"  * {s:<10} (Analysis of Algorithms -- 10 Experiments)")
            elif s == "coa":
                print(f"  * {s:<10} (Computer Organization & Architecture -- 10 Experiments)")
            else:
                print(f"  * {s}")
        print(DIVIDER)
        return

    subject = args[0]
    s = _resolve_subject(subject)
    if s is None:
        print(f"[error] Unknown subject: '{subject}'")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    topics = SUBJECTS[s]
    is_experiment = s in ("aoa", "coa")
    label = "Experiments" if is_experiment else "Topics"

    print(DIVIDER)
    print(f"  {label} in '{s}'")
    print(DIVIDER)
    for num in _valid_topics(s):
        title = topics[num]["title"]
        prefix = f"Exp {int(num):02d}" if is_experiment else f"{num:>2}"
        suffix = " [ASM]" if topics[num].get("code_type") == "asm" else ""
        print(f"  [{prefix}]  {title}{suffix}")
    print(DIVIDER)


def _asm_code(topic):
    if topic.get("code_type") == "asm":
        return topic.get("code", "")
    return topic.get("asm", "")


def _print_asm(topic):
    asm = _asm_code(topic).strip()
    if asm:
        print(asm)
    else:
        print("No assembly program for this experiment.")


def cmd_show(args):
    """show <subject> <topic_num> -- Outputs ONLY the code."""
    args = _normalize_args(args)
    if len(args) < 2:
        print("[error] Usage: python helper.py [show] <subject> <topic_num>")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    raw_subject, raw_topic = args[0], args[1]
    topic = _get_topic(raw_subject, raw_topic)

    if len(args) >= 3 and args[2].lower() in ("asm", "assembly"):
        _print_asm(topic)
        return

    code = topic["code"].strip()
    if code:
        print(code)
    else:
        print("// (no code yet)")


def cmd_asm(args):
    """asm <subject> <topic_num> -- Outputs ONLY the assembly code."""
    args = _normalize_args(args)
    if len(args) < 2:
        print("[error] Usage: python helper.py asm <subject> <topic_num>")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    topic = _get_topic(args[0], args[1])
    _print_asm(topic)


def cmd_write(args):
    """write <subject> <topic_num> [filename]"""
    args = _normalize_args(args)
    if len(args) < 2:
        print("[error] Usage: python helper.py write <subject> <topic_num> [filename]")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    raw_subject, raw_topic = args[0], args[1]
    s = _resolve_subject(raw_subject)
    t = _resolve_topic(s, raw_topic) if s else raw_topic
    topic = _get_topic(raw_subject, raw_topic)

    if len(args) >= 3:
        filename = args[2]
    else:
        if s in ("aoa", "coa"):
            ext = ".asm" if topic.get("code_type") == "asm" else ".c"
            filename = f"{s}_exp_{t}{ext}"
        else:
            filename = f"{s}_topic_{t}.py"

    code = topic["code"]

    try:
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(code.strip() + "\n")
        print(f"[ok] Code written to '{filename}'")
    except OSError as exc:
        print(f"[error] Could not write file: {exc}")
        sys.exit(1)


def cmd_copy(args):
    """copy <subject> <topic_num>"""
    args = _normalize_args(args)
    if len(args) < 2:
        print("[error] Usage: python helper.py copy <subject> <topic_num>")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    raw_subject, raw_topic = args[0], args[1]
    s = _resolve_subject(raw_subject)
    t = _resolve_topic(s, raw_topic) if s else raw_topic
    topic = _get_topic(raw_subject, raw_topic)
    copy_asm = len(args) >= 3 and args[2].lower() in ("asm", "assembly")
    code = _asm_code(topic) if copy_asm else topic["code"]

    is_experiment = s in ("aoa", "coa")
    item_label = "experiment" if is_experiment else "topic"
    if not code.strip():
        print(f"[warn] The code block for this {item_label} is empty - nothing to copy.")
        return

    success = _copy_to_clipboard(code.strip() + "\n")
    display_id = f"Exp {int(t):02d}" if (is_experiment and t and str(t).isdigit()) else t

    if success:
        print(f"[ok] Code for '{s}' {item_label} {display_id} copied to clipboard.")
    else:
        print("[warn] Could not access clipboard (clip, pbcopy, xclip, xsel, tkinter all unavailable).")
        print("       Here is the code snippet:\n")
        print(code)


# -----------------------------------------------------------------------------
#  ENTRY POINT
# -----------------------------------------------------------------------------

USAGE = """\
helper.py -- offline CLI study helper

Usage:
  python helper.py list
  python helper.py list <subject>
  python helper.py show  <subject> <topic_or_exp>
  python helper.py asm   <subject> <topic_or_exp>
  python helper.py write <subject> <topic_or_exp> [filename]
  python helper.py copy  <subject> <topic_or_exp> [asm]

For AOA and COA experiments, you can specify '1', 'exp1', or 'exp 1'.
COA experiments 3, 4, 8, and 9 also include an 8086 assembly program.

Available subjects: {subjects}
"""

COMMANDS = {
    "list":  cmd_list,
    "show":  cmd_show,
    "asm":   cmd_asm,
    "write": cmd_write,
    "copy":  cmd_copy,
}


def main():
    argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE.format(subjects=", ".join(_valid_subjects())))
        sys.exit(0)

    cmd = argv[0].lower()
    rest = argv[1:]

    if cmd in ("show", "code", "get"):
        cmd_show(rest)
    elif cmd in COMMANDS:
        COMMANDS[cmd](rest)
    elif _resolve_subject(cmd):
        # Direct shortcut: python helper.py aoa 1
        cmd_show([cmd] + rest)
    else:
        print(f"[error] Unknown command or subject: '{cmd}'")
        print(f"        Valid commands: {', '.join(COMMANDS)}")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        print()
        print(USAGE.format(subjects=", ".join(_valid_subjects())))
        sys.exit(1)


if __name__ == "__main__":
    main()
