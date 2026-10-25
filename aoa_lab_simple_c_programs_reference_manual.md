# Analysis of Algorithms (AOA) Lab — C Programs Reference Manual
**S.E. (AI & DS) Semester III | Simplified C Implementations with User Input (`scanf`)**

---

## Quick Reference Summary

| Exp. | Topic | Algorithmic Paradigm | Time Complexity | Space Complexity |
| :---: | :--- | :--- | :--- | :--- |
| **01** | Insertion Sort & Selection Sort | Incremental / Comparison | $O(n^2)$ | $O(1)$ |
| **02** | Binary Search (Divide & Conquer) | Divide and Conquer (DAC) | $O(\log n)$ | $O(\log n)$ |
| **03** | Quick Sort (Divide & Conquer) | Divide and Conquer (DAC) | $O(n \log n)$ avg, $O(n^2)$ worst | $O(\log n)$ |
| **04** | Fractional Knapsack | Greedy Method | $O(n^2)$ | $O(n)$ |
| **05** | Prim's Minimum Spanning Tree (MST) | Greedy Method | $O(V^2)$ | $O(V^2)$ |
| **06** | Floyd-Warshall All-Pairs Shortest Path | Dynamic Programming | $O(V^3)$ | $O(V^2)$ |
| **07** | Sum of Subset | Backtracking | $O(2^n)$ | $O(n)$ |
| **08** | N-Queens Placement | Backtracking | $O(N!)$ | $O(N)$ |
| **09** | Rabin-Karp String Matching | Rolling Hash / String Matching | $O(n + m)$ avg, $O(nm)$ worst | $O(1)$ |
| **10** | Min-Max Finding (Divide & Conquer) | Divide and Conquer (DAC) | $O(n)$ [$3n/2 - 2$ comparisons] | $O(\log n)$ |

---

### Terminal Quick Reference
- **Compile:** `gcc filename.c -o solution`
- **Execute (Windows):** `.\solution.exe`
- **Execute (Linux/macOS):** `./solution`

---

## Experiment 01: Insertion Sort and Selection Sort

- **Paradigm:** Comparison Sorting / Incremental
- **Time Complexity:** $O(n^2)$
- **Space Complexity:** $O(1)$

```c
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
```

### Sample Input & Output
```text
Enter number of elements: 5
Enter 5 integers: 64 25 12 22 11
Choose (1 for Insertion Sort, 2 for Selection Sort): 1
Sorted array: 11 12 22 25 64
```

---

## Experiment 02: Binary Search using Divide and Conquer

- **Paradigm:** Divide and Conquer (DAC)
- **Time Complexity:** $O(\log n)$
- **Space Complexity:** $O(\log n)$

```c
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
```

### Sample Input & Output
```text
Enter number of elements: 6
Enter 6 sorted elements: 10 20 35 50 65 80
Enter element to search: 50
Success: 50 found at index 3 (position 4).
```

---

## Experiment 03: Quick Sort using Divide and Conquer

- **Paradigm:** Divide and Conquer (DAC)
- **Time Complexity:** $O(n \log n)$ Average, $O(n^2)$ Worst
- **Space Complexity:** $O(\log n)$

```c
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
```

### Sample Input & Output
```text
Enter number of elements: 6
Enter 6 elements: 28 14 45 7 32 19
Sorted array (Quick Sort): 7 14 19 28 32 45
```

---

## Experiment 04: Fractional Knapsack using Greedy Method

- **Paradigm:** Greedy Method
- **Time Complexity:** $O(n^2)$
- **Space Complexity:** $O(n)$

```c
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
```

### Sample Input & Output
```text
Enter number of items: 3
Item 1 (Profit Weight): 25 18
Item 2 (Profit Weight): 24 15
Item 3 (Profit Weight): 15 10
Enter knapsack capacity: 20
Maximum Profit = 31.50
```

---

## Experiment 05: Prim's Minimum Spanning Tree (MST) Algorithm

- **Paradigm:** Greedy Method
- **Time Complexity:** $O(V^2)$
- **Space Complexity:** $O(V^2)$

```c
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
```

### Sample Input & Output
```text
Enter number of vertices: 4
Enter cost matrix (use 0 for self/no edge):
0 2 0 6
2 0 3 8
0 3 0 5
6 8 5 0

Selected MST Edges:
Edge 1: (0 -> 1) with Cost = 2
Edge 2: (1 -> 2) with Cost = 3
Edge 3: (2 -> 3) with Cost = 5
Total MST Cost = 10
```

---

## Experiment 06: All-Pairs Shortest Path (Floyd-Warshall)

- **Paradigm:** Dynamic Programming
- **Time Complexity:** $O(V^3)$
- **Space Complexity:** $O(V^2)$

```c
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
```

### Sample Input & Output
```text
Enter number of vertices: 4
Enter weighted matrix (use 999 for INF):
0 3 999 7
8 0 2 999
5 999 0 1
2 999 999 0

All-Pairs Shortest Distance Matrix:
0	3	5	6	
5	0	2	3	
3	6	0	1	
2	5	7	0	
```

---

## Experiment 07: Sum of Subset using Backtracking

- **Paradigm:** Backtracking
- **Time Complexity:** $O(2^n)$
- **Space Complexity:** $O(n)$

```c
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
```

### Sample Input & Output
```text
Enter number of elements: 4
Enter 4 positive integers: 3 4 5 6
Enter target sum: 9

Subsets summing to 9:
{ 3 6 }
{ 4 5 }
```

---

## Experiment 08: N-Queens Problem using Backtracking

- **Paradigm:** Backtracking
- **Time Complexity:** $O(N!)$
- **Space Complexity:** $O(N)$

```c
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
```

### Sample Input & Output
```text
Enter number of Queens (N): 4

Solution board placement:
. Q . . 
. . . Q 
Q . . . 
. . Q . 
```

---

## Experiment 09: Rabin-Karp String Matching Algorithm

- **Paradigm:** Rolling Hash / String Matching
- **Time Complexity:** $O(n + m)$ Average, $O(nm)$ Worst
- **Space Complexity:** $O(1)$

```c
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
```

### Sample Input & Output
```text
Enter text string (no spaces): AABAACAADAABAABA
Enter pattern to search: AABA
Pattern found at index 0
Pattern found at index 9
Pattern found at index 12
```

---

## Experiment 10: Min-Max Algorithm using Divide and Conquer

- **Paradigm:** Divide and Conquer (DAC)
- **Time Complexity:** $O(n)$ with exactly $3n/2 - 2$ comparisons
- **Space Complexity:** $O(\log n)$

```c
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
```

### Sample Input & Output
```text
Enter number of elements: 8
Enter 8 elements: 15 8 20 5 12 30 2 18
Minimum element = 2
Maximum element = 30
```