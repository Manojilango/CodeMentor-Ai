def maxAmount(i, j, arr):
    # Base case: If i > j, no more elements are left to pick
    if i > j:
        return 0

    # Option 1: Take the first element arr[i]
    takeFirst = arr[i] + min(maxAmount(i + 2, j, arr),
                             maxAmount(i + 1, j - 1, arr))

    # Option 2: Take the last element arr[j]
    takeLast = arr[j] + min(maxAmount(i + 1, j - 1, arr),
                            maxAmount(i, j - 2, arr))

    return max(takeFirst, takeLast)

def maximumAmount(arr):
    n = len(arr)
    res = maxAmount(0, n - 1, arr)
    return res

#Driver Code Starts

if __name__ == "__main__":
    arr = [5, 3, 7, 10]
    res = maximumAmount(arr)
    print(res)

#Driver Code Ends