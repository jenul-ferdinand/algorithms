# Sorting Complexity

Given the knowledge we've gained on algorithms and their time complexity, let us analyse the complexity of the three basic sorting algorithms we have seen so far, namely Bubble Sort, Selection Sort, and Insertion Sort.

> Before we start, recall that the input to each of these sorting algorithms is a collection of elements, i.e. an array or a list that we need to sort, which means the complexity of these algorithms should be measured with respect to the number nn of elements in the collection.

> Additionally, from now on we will be interested in analysing the best-case and the worst-case complexity of an algorithm. These literally mean what happens with the algorithm in the best-case and worst-case scenarios given an input of size n, which is normally easy to see by checking the algorithm's flow, i.e. whether or not the algorithm has some if conditions affecting the number of elementary operations. You will see this in the analysis of Bubble Sort II below.

> We should point out to one major mistake sometimes made by students: you may think the best case occurs when the input is small while the worst case occurs when the input is large. Note that this understanding of the best-case and worst-case complexity is wrong because in both best- and worst- cases we must assume the input is of size n.

## A few simple assumptions

Before we get to analysis of the sorting algorithms, let's make a few preliminary observations. All the algorithms we are interested in - in this unit make extensive use of item _comparison_ and _swapping_. The implementation of element swapping can be done in the following way:

```py
def swap(the_list, i, j):
    temp = the_list[i]
    the_list[i] = the_list[j]
    the_list[j] = temp
```

Observe that no matter what size `the_list` has, the `swap()` operation makes a constant number of elementary operations. Namely, copying a value from one variable to another requires _reading_ the value from the original variable and _writing_ it into the new variable, which is done three times. Hence, the complexity of `swap()` is constant, i.e., O(1).

> Python's syntax enables us to do `the_list[i], the_list[j] = the_list[j], the_list[i]`, which looks cleaner and behaves identically to calling `swap()` above.

As for item comparison, it is an elementary operation that in general costs _linear time_ on the _size of the items_. For instance, this holds for string-typed items where we have to traverse the characters of two strings being lexicographically compared one by one. However, in this unit when analysing the _complexity of sorting algorithms_, we will restrict our analysis to _numeric items of fixed size_ only, and the cost of the comparison in this case will be assume to be constant, i.e., O(1).

## Bubble Sort

### Bubble Sort I

<p align="center">
    <img width="300px" src="https://upload.wikimedia.org/wikipedia/commons/archive/c/c8/20131109191604%21Bubble-sort-example-300px.gif"/>
</p>

Let us start with the most _naive_ version of Bubble Sort that does not implement any optimisations. It looks as follows: 

```py
def bubble_sort(arr);
    n = len(arr)
    for _ in range(n-1):
        for i in range(n-1):
            if arr[i] > arr[i+1]:
                swap(arr, i, i+1)
```

Also observe that Bubble Sort constitutes two loops. The outer loop iterates $n-1$ times, with $n$ being the length of the list to be sorted. The inner loop also iterates $n-1$ times, which makes the total number of iterations become $(n-1)^2$, which grows as $O(n^2)$. Now, every such iteration makes a comparison of items at positions `i` and `i+1`, which according to our assumption is done at constant time. So far the overall complexity adds up to $O(n^2)$.

The number of times the `swap()` operation is invoked depends on how many times the comparison return true. For instance, if the collection is already sorted, the comparison always returns false and no swapping is required; on the contrary, if the collection is sorted in reversed order then each of the $(n-1)^2$ iterations invokes `swap()`. But no matter how many times `swap()` is executed, the overall complexity of Bubble Sort I is still $O(n^2)$ because swapping contributes constant time in each iteration. This means that there is no difference between the best-case and worst-case complexity here.

### Bubble Sort II

<p align="center">
    <img width="300px" src="https://upload.wikimedia.org/wikipedia/commons/c/c8/Bubble-sort-example-300px.gif"/>
</p>

Note that Bubble Sort II will make use of several optimisations, including (a) _the reduction of the number of iterations of the inner loop_ and (b) _the use of an early termination condition_:

```py
def bubble_sort(arr):
    n = len(arr)

    for mark in range(n-1, 0, -1):
        swapped = False

        for i in range(mark): # (a) iterate mark times rather than n-1 times
            if arr[i] > arr[i+1]:
                swap(arr, i, i+1)
                swapped = True

        if not swapped: # (b) early termination, if no swap is done this time
            break
```

In contrast to Bubble Sort I, the number of times the outer loop iterates depends on the early termination condition. If there is no swapping done during the current iteration of the outer loop then the algorithm immediately stops.

This highlights the **best-case scenario**, i.e., when the collection is _already_ sorted the way we want and so no swapping is needed. In this case, we make a single iteration of the outer loop, which runs the inner loop for $n-1$ times. As previously, each of these $n-1$ inner iterations contributes constant time to the overall complexity due to the comparison check. As a result, the best-case complexity is $O(n)$.

In the worst-case, i.e., when at least one swap is done in each outer iteration, the outer loop iterates $n-1$ times. The **worse-case scenario** occurs, for instance, when the collection is sorted in the opposite order. Let's see how many times the algorithm iterates in this case. Note that the inner loop iterates `mark` times, which is decremented in each iteration of the outer loop. This way, the inner loop iterates $n-1$ times, then $n-2$ times, then $n-3$ times, and so on, till 1 time (in the last iteration of the outer loop). This adds up in the total number of iterations that can be computed as the [arithmetic series](https://en.wikipedia.org/wiki/Arithmetic_progression):

$$(n-1) + (n-2) + ... + 1 = \frac{(n-1+1)\cdot(n-1)}{2} = \frac{n^2-n}{2} = O(n^2)$$

The above suggests that in the worst case, the total number of iterations still grows as $O(n^2)$ and each such iteration (as before) spends constant time performing comparison and swapping, adding up to the total worst-case complexity being $O(n^2)$.

> As a result, the overall **best-case complexity** of Bubble Sort II is $O(n)$ while its **worst-case complexity** is $O(n^2)$.

## Selection Sort

<p align="center">
    <img height="200px" src="https://upload.wikimedia.org/wikipedia/commons/9/94/Selection-Sort-Animation.gif"/>
</p>

The complexity analysis for Selection Sort is pretty simple. Here is our implementation of this algorithm:

```py
def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_index = find_min_index(arr, i)
        swap(arr, i, min_index)
```

Semantically, the algorithm iteratively picks the i'th minimal item in the collection and puts it into its correct position, i.e., into position `i`. This way, the first $k$ iterations result in $k$ items being in their correct positions. Observe that the loop above iterates $n-1$ times, each time making a call to `find_index_min()` and then to `swap()`. While the latter contributes constant time in each iteration, the former's contribution is analysed next. This is how `find_index_min()` is implemented.

```py
def find_index_min(arr, start):
    pos_min = start
    n = len(arr)
    for i in range(start + 1, n):
        if arr[i] < arr[pos_min]:
            pos_min = i
    return pos_min
```

As with the inner loop of Bubble Sort II, the loop in this function iterates a varying number of times, depending on the iteration of the main loop of Selection Sort. Namely, when it is called by `selection_sort()` the first time, `start = 0` and so there are $n-1$ iterations here. Next time, `start = 1` and the loop iterates $n-2$. And so on, until we get to the last time it is called with `start = n - 2`, which makes the loop iterate once. This results in the same arithmetic series $1 + ... + (n-2) + (n-1) = \frac{n^2-n}{2}$. Each such iteration performs constant-time operations of item comparion and arithmetic assignment.

Overall, this adds up to $O(n^2)$ time complexity of Selection Sort. Observe that the algorithm does not have any early termination conditions that would differentiate the best-case from the worst-case. This algorithm always makes $O(n^2)$ elementary steps on inputs of size $n$.

## Insertion Sort

<p align="center">
    <img width="300px" src="https://upload.wikimedia.org/wikipedia/commons/9/9c/Insertion-sort-example.gif"/>
</p>

The complexity analysis for Insertion Sort is somewhat similar to that of Bubble Sort II and results in separate best- and worst-case complexity. Recall our implementation of Insertion Sort. It has two loops, one nested in the other, and it looks as follows:

```py
def insertion_sort(arr):
    n = len(arr)
    for mark in range(1, n): # n - 1 iterations
        temp = arr[mark]
        i = mark - 1
        while i >= 1 and arr[i] > temp: # number of times depends...
            arr[i+1] = arr[i]
            i -= 1
        arr[i + 1] = temp
```

On the high level, the algorithm can be seen as dividing the target collection of items into two parts: (1) sorted and (2) unsorted. The outer loop of the algorithm iteratively picks an unsorted element and then inserts it in the correct position in the sorted part. This way, each iteration of the algorithm extends the sorted part by one item.

Picking a new element is done by means of the outer loop, which makes exactly $n-1$ iterations while the insertion operation consists of two parts:

1. Finding the correct position for the newly selected item and shuffling the larger items in the sorted part, which is done by the inner loop.

2. Copying the newly selected item into the identified position.

Note that the latter copying performs a single constant-time operation. Each iteration of the inner loop is also constant-time. So the only thing left to understand is how many times the inner loops iterates given an item selected by the outer loop. Recall that we iterate until either we traverse all the items in the sorted part (in this case, the newly selected item should be placed at position 0) or we find an item not larger than the newly selected one. This is where the best-case and the worst-case differ.

The **best-case** occurs when our collection is already sorted and so each newly selected item _already_ sits in its correct position and so the inner loop stops _immediately_. In this case, the total number of elementary operations performed by  the algorithm is $O(n)$ as dictated by the outer loop.

On the contrary, the **worst-case scenario** occurs when the collection is sorted in reverse. Here, assuming we are in iteration $k$ of the outer loop, each newly selected item has to be inserted into position $0$ and so the inner loop has to iterate $k$ times and shuffling the already sorted items accordingly. Observe that in this case the inner loop makes $1$ iteration when `mark = 1`, followed by $2$ iterations when `mark = 2`, followed by $3$ iterations when `mark = 3`, and so on until `mark = n - 1`, in which case the inner loops makes $n-1$ iterations. This looks like what we have already seen: $1+2+...+(n-1)=\frac{n^2-n}{2}=O(n^2)$.

> As a result, the overall **best-case complexity** of Insertion Sort is $O(n)$ while its **worst-case complexity** is $O(n^2)$.

# Final Remarks

Although the worst-case complexity of these algorithms is the same and equals $O(n^2)$, Insertion Sort is often preferred in the cases where _partially sorted_ data is considered. This is because little needs to be done for the items already sitting in their correct positions: The algorithm avoids making many comparison and swapping/shuffling operations. On the other hand, when memory access is slow and there is a lot of shuffling to perform, which is the case for _poorly sorted_ data, one may want to opt for Selection Sort. Can you figure why?

The reason is that, Selection Sort performs exactly $O(n)$ swaps to place each element into its final, sorted position in each pass. The inner loop will do many comparisons, but only one write (swap) operation will be done at the end of the outer loop iteration. Insertion Sort, on the other hand, performs many shifts of elements to ensure that there is space for the element being inserted into its final sorted position. In the worst case (a reverse-sorted array), this can result in up to $O(n^2)$ memory writes.