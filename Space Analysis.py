"""
Space Analysis - Solution.
Lesson 2 Practise Exercise: Classify Space complexity and compare memory trade-offs.
"""

import random
import time 


# ====================================
# Part 1: Space Complextity Classifications
# ====================================

# O(n) space - creating a new string of the same length as input.
# The slice s[::-1] allocates a fresh sting object proportional to len(s).
def reverse_sting(s):
    return s[::-1] 


# O(k) space - where k is the number of unique characters in the text.
# Worst case k == n (all unique characters), but k is bounded by the alphabet size. It is (O(1))
# We write O(k) to be precisel the dict grows only as big as the character variety. 
def count_letter(text):
    freq = {}                                       # dict grown to at most k entries
    for ch in text:                                 
        freq[ch] = freq.get(ch, 0) + 1
    return freq 



# O(n²) space - we allocate an nxn 2-D list.
# Total cells = n * n = n². 
def matrix_identity(n):
    matrix = [[0] * n for _ in range(n)]            # n rows x n columns -> n² integers 
    for i in range(n):
        matrix[i][i] = 1
    return matrix


# O(1) space - only a single accumulator variable is used. 
# Memory usage is constant regardless of how long 'numbers' is.
def running_sum(numbers):
    total = 0                                       # one variable - O(1)
    for x in numbers: 
        total += x
    return total


print("=" * 60)
print("PART 1: Space Comlexity Classifications")
print("=" * 60)
space_classifications = [
    ("recers_string(s)",    "O(n)", "New string allocated to input length"),
    ("count_letters(text)", "O(k)",  "Dict size = unique character count(bounded by alphabet)"),
    ("matrix_identity(n)",  "O(n²)",    "Full nxn matrix allocated in memory"),
    ("running_sum(numbers)",    "O(1)", "Single accumulator variable - constant memory"),
]
for name, complexity, reason in space_classifications:
    print(f" {name:<30} {complexity:<8} {reason}")
    
    
# =======================================
# PART 2: Duplicate Email Detection - Time/Space Trade-offs
# =======================================

# --- Generate sample data ---
NUM_EMAILS = 10_000
domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
# Create 8,000 unique emails then repeat 2,000 of them to guarantee duplicates
unique_emails = [f"user{i}@{domains[i % len(domains)]}" for i in range(8_000)]
duplicates = random.choices(unique_emails, k=2_000)
all_emails = unique_emails + duplicates
random.shuffle(all_emails)


# ---- Approach 1: Set-based ----
# Time: O(n)    - one pass; set add/lookup are O(1) average
# Space: O(n)   - the set can hold up to n email strings
#
# Best when: you have plenty of RAM and want the fastest runtime.
def find_duplicates_set(emails):
    """Return a set of email addressses that appear more than once."""
    #O(n) time - single pass throught the list
    #O(n) space - set grows proportionally to the number of unique emails
    seen = set()
    duplicates = set()
    for email in emails:
        if email in seen:
            duplicates.add(email)
        else:
            seen.add(email)
    return duplicates


# ---- Approach 2: Sort-and-scan ----
# Time: O(n log n) - dominated by the sort step
# Space: O(1) extra - sorted() in Python creates new list (O(n) total).
#
# Best when: RAM is scarce (e.g., 4 GB) and you can afford the slower sort.
# ON a 64GB machiene the set approach is almost always prefered with higher RAM.
def find_duplicates_sort(emails):
    """Return a set of email addresses that appear more than once."""
    # O (n log n) time - sort dominates
    # O(1) extra space - scan adjacent elements after sorting
    sorted_emails = sorted(emails)      # O(n log n) time, O(n) for the sorted copy
    duplicates = set()
    for i in range(1, len(sorted_emails)):
        if sorted_emails[i] == sorted_emails[i - 1]:
            duplicates.add(sorted_emails[i])
    return duplicates 



# --- Benchmark both approaches ---
def benchmark(func, data, label):
    start = time.time()
    result = func(data)
    elapsed = (time.time() - start) * 1000
    return result, elapsed


print("\n" + "=" * 60)
print(f"PART 2: Duplicate Email Detection ({NUM_EMAILS:,} rows)")
print("=" * 60)

dupes_set, t_set = benchmark(find_duplicates_set, all_emails, "Set approach")
dupes_sort, t_sort = benchmark(find_duplicates_sort, all_emails, "Sort+scan approach")

print(f" Set approach   :   {len(dupes_set):>5} duplicates found in {t_set:.3f} ms")
print(f" Sort+scan  : {len(dupes_sort):>5} duplicates found in {t_sort:.3f} ms")
print(f" Both agree : {dupes_set == dupes_sort}")

print("""
      Memory strategy: 
      4 GM RAM -> Prefer sort-and-scan (avoids loading all emails into a set)
      64GB RAM -> Prefer set approach (faster O(n) vs )(n log n), RAM is not constraint)
      """)