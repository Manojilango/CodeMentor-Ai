def dailyTemperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []

    for i in range(len(temperatures)):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        stack.append(i)

    return result


temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(dailyTemperatures(temps))
# expected: [1, 1, 4, 2, 1, 1, 0, 0]