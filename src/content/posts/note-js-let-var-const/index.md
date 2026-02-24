---
title: '[note] JS變數宣告 let / var / const'
published: 2021-07-16
description: '整理 JavaScript 變數宣告 let、var、const 的作用域差異、TDZ 暫時性死區與常見面試考題。'
tags: ['javascript', 'frontend']
author: 'Pei Wang'
draft: false
---

![圖文不符：基隆海邊 好久沒拍底片了啊](https://cdn-images-1.medium.com/max/800/1*pni7Ql1XM8wt02NgcXpmDA.jpeg)

看 [JavaScript 全攻略：克服 JS 的奇怪部分](https://www.udemy.com/course/javascriptjs/) 課程時，課程範例多為 var，但我自己是從 let、const 學起，習慣用後者來取代前者，卻發現出來的結果和課程不一樣，便是因為 var 和 let、const 有著天差地遠的差別！

堪稱基礎中的基礎的變數宣告，也是常見面試考題

以下取自 MDN 對 ES6 let const 的範例，以及參考網路上各位大大的文章後，整理出來的筆記

參考資料：

- [JavaScript 全攻略：克服 JS 的奇怪部分](https://www.udemy.com/course/javascriptjs/)
- [MDN let - JavaScript](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Statements/let)
- [JavaScript基本功修練：Day5 - 宣告變數 - let、const、var](https://ithelp.ithome.com.tw/articles/10216834)（強烈推薦，舉例多且說明清楚）

---

## var 作用域是 function，let / const 作用域是區塊 block

差別在 scope 的不同

### var（function）

- 作用域是 function 函數，函數若有重複區塊，會產生變數衝突
- 可以重複宣告
- 往外層找 function，若外層沒有 function，則變成全域性
- 會變成全域變數，用 window 物件呼叫

⚠️ 在 if / else / for / while 中使用 var，會汙染全域變數，難以維護，而 let / const 解決了這個問題

### let（block）

- 作用域為區塊 block，一個 function 中若有區塊相隔，可以有 2 個同樣變數的 let
- 區塊作用域（block scope），也就是 `{ }` 包住的區域
- 禁止同層重複宣告

### const

- 作用域為區塊，一個 function 中若有區塊相隔，可以有 2 個同樣變數的 const
- let 加強版
- 禁止同層重複宣告
- 常數保護，不能修改（重新賦值）
- 在宣告 const 時就必定要指定給值

## 作用域不同，可能會產生變數衝突

```javascript
function varTest() {
  var x = 1
  {
    var x = 2 // 同樣是變數 x
    console.log(x) // 2
  }
  console.log(x) // 2 跟著上面一起被覆蓋
}
// var 的範圍是 function，第一個 x 和第二個 x 會互相衝突覆蓋
// 因此第一個 x 也被覆蓋為 2
```

```javascript
function letTest() {
  let x = 1
  {
    let x = 2 // 雖然命名都是 x，但存在於不同記憶體，不同變數
    console.log(x) // 2
  }
  console.log(x) // 1
}
// 不同區塊間的變數不會互相影響
```

let 作用域為區塊，跳出 if 條件式後，變數 `b=22` 便不存在，會取用在全域的 `b=2`。

var 作用域為 function，若往外層找沒有 function，則會做為全域變數，此時 if 條件式中的 `var a=11` 就是全域變數。

```javascript
var a = 1
var b = 2

if (a === 1) {
  var a = 11 // 全域變數
  let b = 22 // 只存在 if 區塊內

  console.log(a) // 11
  console.log(b) // 22
}

console.log(a) // 11
console.log(b) // 2
```

## let 無法在 global 物件下建立 property 屬性

```javascript
var x = 'global'
let y = 'global'
console.log(this.x) // "global"
console.log(this.y) // undefined
```

## let 不能重複宣告

重複宣告會產生 `SyntaxError` 的警告

```javascript
if (x) {
  let foo
  let foo // SyntaxError thrown.
}
```

switch 可以寫成一個區塊，但會發生重複宣告的情況。此時可以將 case 後的程式用區塊隔開，就可以避免重複宣告

```javascript
// ❌ switch 是一個區塊，會重複宣告
let x = 1
switch (x) {
  case 0:
    let foo
    break
  case 1:
    let foo // SyntaxError for redeclaration.
    break
}

// ✅ 將 case 分別寫成不同區塊
let x = 1
switch (x) {
  case 0: {
    let foo
    break
  }
  case 1: {
    let foo
    break
  }
}
```

## TDZ 暫時性死區

`let` / `const` / `var` 宣告變數時，會提升到作用域的最高處（hoisting）。

不同的是，如果沒宣告就使用：

- `var` 會回傳 `undefined`
- `let` / `const` 會**報錯**

```javascript
var a = 10
function testVar() {
  console.log(a) // Uncaught ReferenceError: Cannot access 'a' before initialization
  let a
}
testVar()
```

以為 `a` 會回傳 10，但 `let` 已經讓 `a` 提升到 function 的最高處，因為變數 `a` 是在後面才宣告，所以會報錯：不能在初始化變數前使用 a

```javascript
var a = 10
function test() {
  console.log(a) // Uncaught ReferenceError: Cannot access 'a' before initialization
  const a = 5
}
test()
```

`const` 也是一樣。

### let 和 const 雖然和 var 一樣有提升的作用，但 let / const 不會有 undefined 的預設值

> Unlike variables declared with var, which will start with the value undefined, let variables are not initialized until their definition is evaluated. Accessing the variable before the initialization results in a ReferenceError. The variable is in a "temporal dead zone" from the start of the block until the initialization is processed.

只有當 `let` 被宣告執行時，變數才可以被使用

```javascript
var a = 10
function testVar() {
  let a
  console.log(a) // undefined
}
testVar()
```

`const` 則是一定要賦值，才可以被使用

```javascript
function test() {
  const a
  console.log(a) // Uncaught SyntaxError: Missing initializer in const declaration
}
test()
```

函數中的變數提升到作用域最高處時，還沒宣告變數的時間，稱為 **TDZ 暫時性死區**，這個時間不能使用未宣告的變數

```javascript
function test() {
  // 提升變數 a
  // TDZ 開始，不能訪問變數 a
  console.log(a) // ReferenceError

  // 宣告變數，TDZ 結束
  let a = 10
}
test()
```

根據 Google 的 JavaScript Style Guide，應該默認用 `const`，如果該變數需要重新被賦值才用 `let`，永遠不用 `var`。

> Declare all local variables with either const or let. Use const by default, unless a variable needs to be reassigned. The var keyword must not be used.

## 更改不是指值的更改，而是記憶體地址的更改

決定那個變數會變，還是不變，是指那個變數的**記憶體地址**有沒有變，而不是它的值

- **基本型別值**（字串、數值、`undefined`、`null`、symbol）：不能更改它的值，只能重新賦值，重新賦值時會更改記憶體地址
- **引用值**（物件、陣列、函式）：能修改它裡面的值，這樣不會更改記憶體地址，但如果重新賦予一個新的值，就會更改記憶體地址

以下兩個例子都是值的改變，但並沒有改變記憶體位置，所以 `const` 不會報錯：

```javascript
const x = []
x.push(1, 2, 3, 4) // ✅ 修改陣列內容，記憶體地址不變

const y = { name: 'Mary', age: 30 }
y.name = 'Peter' // ✅ 修改物件屬性，記憶體地址不變
```
