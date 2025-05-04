
def find_median_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    x, y = len(nums1), len(nums2)

    low = 0
    high = x

    while low <= high:
        partition_x = (low + high) // 2
        partition_y = (x + y + 1) // 2 - partition_x

        # If partition_x is 0 it means nothing is there on left side. Use -inf for max_left_x
        # If partition_x is length of array then there is nothing on right side. Use +inf for min_right_x
        max_left_x = float('-inf') if partition_x == 0 else nums1[partition_x - 1]
        min_right_x = float('inf') if partition_x == x else nums1[partition_x]

        max_left_y = float('-inf') if partition_y == 0 else nums2[partition_y - 1]
        min_right_y = float('inf') if partition_y == y else nums2[partition_y]

        if max_left_x <= min_right_y and max_left_y <= min_right_x:
            if (x + y) % 2 == 0:
                return (max(max_left_x, max_left_y) + min(min_right_x, min_right_y)) / 2
            else:
                return max(max_left_x, max_left_y)
        elif max_left_x > min_right_y:
            high = partition_x - 1
        else:
            low = partition_x + 1

    raise ValueError("Input arrays are not sorted correctly or invalid.")

def smart_cast(s):
    try:
        f = float(s)
        return int(f) if f.is_integer() else f
    except ValueError:
        return s  # or raise an error

if __name__ == '__main__':
    f = [smart_cast(x) for x in input("input1: ").split()]
    s = [smart_cast(x) for x in input("input2: ").split()]

    print("output: ", smart_cast(find_median_sorted_arrays(f, s)))

    # Space complexity: O(1)
    # Time complexity: O(log(min(n, m)))