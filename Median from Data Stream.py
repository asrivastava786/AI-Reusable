import heapq

class MedianFinder:

    def __init__(self):
        self.small = []  # max heap using negative values
        self.large = []  # min heap

    def addNum(self, num: int) -> None:
        # Step 1: add to max heap
        heapq.heappush(self.small, -num)

        # Step 2: move largest from small to large
        heapq.heappush(self.large, -heapq.heappop(self.small))  # So if large becomes bigger, move one number back from large to small.

        # Step 3: keep small same size or one bigger
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]

        return (-self.small[0] + self.large[0]) / 2

#small = smaller half, max heap
#large = larger half, min heap

#small can have one extra element
#median comes from heap tops
