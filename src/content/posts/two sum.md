---
title: two sum
published: 2026-02-26
description: 'leetcode easy: two sum 解法'
tags: ['leetcode', 'easy']
author: Pei Wang
draft: false
created: 2026-02-25
---

> 題目 https://leetcode.com/problems/two-sum/description/

## 暴力解

**Complexity Analysis**

- Time complexity: O(n2).
- Space complexity: O(1).

```js
var twoSum = function (nums, target) {
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] === target) return [i, j]
    }
  }
}
```

## Map 紀錄差值

檢查 target 和 loop 的數字差值是否有被記錄到 map 裡，如果已經存在就會return order。如果不存在（代表 order 靠前），會將判斷過不匹配的數字儲存，等待後面數字配對

- Time complexity: O(n).
  - Map has 和 get 都是 O(1)
- Space complexity: O(n).

```js
var twoSum = function (nums, target) {
  const map = new Map()
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i]
    if (map.has(complement)) return [map.get(complement), i]
    map.set(nums[i], i)
  }
}
```
