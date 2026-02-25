---
title: FizzBuzz
published: 2026-02-25
description: leetcode eazy
tags: ['leetcode', 'easy']
author: Pei Wang
draft: false
created: 2026-02-25
---

https://leetcode.com/problems/fizz-buzz/description/

```js
var fizzBuzz = function (n) {
  let arr = []
  for (let i = 1; i <= n; i++) {
    let str = ''
    if (i % 3 === 0) str += 'Fizz'
    if (i % 5 === 0) str += 'Buzz'
    arr.push(String(!str ? i : str))
  }
  return arr
}
```
