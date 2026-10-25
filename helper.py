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
        printf("Item %d profit: ", i + 1);
        scanf("%f", &profit[i]);

        printf("Item %d weight: ", i + 1);
        scanf("%f", &weight[i]);

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

    "subject2": {
        "1": {
            "title": "Topic 1 Title",
            "notes": "Core logic and steps for subject2 topic 1.",
            "code": """\
""",
        },
        "2": {
            "title": "Topic 2 Title",
            "notes": "Core logic and steps for subject2 topic 2.",
            "code": """\
""",
        },
        "3": {
            "title": "Topic 3 Title",
            "notes": "Core logic and steps for subject2 topic 3.",
            "code": """\
""",
        },
        "4": {
            "title": "Topic 4 Title",
            "notes": "Core logic and steps for subject2 topic 4.",
            "code": """\
""",
        },
        "5": {
            "title": "Topic 5 Title",
            "notes": "Core logic and steps for subject2 topic 5.",
            "code": """\
""",
        },
        "6": {
            "title": "Topic 6 Title",
            "notes": "Core logic and steps for subject2 topic 6.",
            "code": """\
""",
        },
        "7": {
            "title": "Topic 7 Title",
            "notes": "Core logic and steps for subject2 topic 7.",
            "code": """\
""",
        },
        "8": {
            "title": "Topic 8 Title",
            "notes": "Core logic and steps for subject2 topic 8.",
            "code": """\
""",
        },
        "9": {
            "title": "Topic 9 Title",
            "notes": "Core logic and steps for subject2 topic 9.",
            "code": """\
""",
        },
        "10": {
            "title": "Topic 10 Title",
            "notes": "Core logic and steps for subject2 topic 10.",
            "code": """\
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
        label = "experiment" if s == "aoa" else "topic"
        print(f"[error] Unknown {label} identifier: '{topic_num}' for subject '{s}'")
        valid_items = [f"exp{k}" if s == "aoa" else k for k in _valid_topics(s)]
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
    is_aoa = (s == "aoa")
    label = "Experiments" if is_aoa else "Topics"

    print(DIVIDER)
    print(f"  {label} in '{s}'")
    print(DIVIDER)
    for num in _valid_topics(s):
        title = topics[num]["title"]
        prefix = f"Exp {int(num):02d}" if is_aoa else f"{num:>2}"
        print(f"  [{prefix}]  {title}")
    print(DIVIDER)


def cmd_show(args):
    """show <subject> <topic_num> -- Outputs ONLY the code."""
    args = _normalize_args(args)
    if len(args) < 2:
        print("[error] Usage: python helper.py [show] <subject> <topic_num>")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    raw_subject, raw_topic = args[0], args[1]
    topic = _get_topic(raw_subject, raw_topic)
    code = topic["code"].strip()
    if code:
        print(code)
    else:
        print("// (no code yet)")


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
        if s == "aoa":
            filename = f"aoa_exp_{t}.c"
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
    code = topic["code"]

    item_label = "experiment" if s == "aoa" else "topic"
    if not code.strip():
        print(f"[warn] The code block for this {item_label} is empty - nothing to copy.")
        return

    success = _copy_to_clipboard(code.strip() + "\n")
    display_id = f"Exp {int(t):02d}" if (s == "aoa" and t and str(t).isdigit()) else t

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
  python helper.py write <subject> <topic_or_exp> [filename]
  python helper.py copy  <subject> <topic_or_exp>

For AOA experiments, you can specify '1', 'exp1', or 'exp 1'.

Available subjects: {subjects}
"""

COMMANDS = {
    "list":  cmd_list,
    "show":  cmd_show,
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
