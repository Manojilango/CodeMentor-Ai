def binary_search(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


nums = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(nums, 7))    # expected: 3
print(binary_search(nums, 11))   # expected: 5
print(binary_search(nums, 4))    # expected: -1 (not in array)