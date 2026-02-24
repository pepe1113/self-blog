---
title: '[筆記]slick.js做出商品照輪播'
published: 2021-05-16
description: '使用 slick.js 套件做出商品照垂直縮圖輪播效果的筆記，包含常用設定與事件說明。'
tags: ['javascript', 'frontend']
author: 'Pei Wang'
draft: false
---

![](https://cdn-images-1.medium.com/max/800/1*SaGta1x8brX4Gx0KGr2S1g.png)

```
Slick.js http://kenwheeler.github.io/slick/
```

投影片輪播的套件，之前都是使用六角介紹的 [swiper](https://swiperjs.com/demos)，官方文件和demo都很詳細，相當推薦

為了做出其他商品照輪播的效果，又從codepen找到完全是我要的slick做的輪播效果，像下面這張圖，同樣類似效果也可以在uniqlo商品頁面看到

玩出來的效果很實用，作為使用者體驗也不錯

![左側小圖會隨著點擊往上滑動一格](https://cdn-images-1.medium.com/max/800/1*wniohWmzHAJoh-R-o7bMJw.png)

![左下小圖可點擊，看到更多商品細節](https://cdn-images-1.medium.com/max/800/1*-nXsDvsIwIEOsL5C8o5sKQ.png)

## 安裝

CDN，需裝入 jquery

```html
<!-- CSS -->
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.css"
/>
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick-theme.min.css"
/>

<!-- jQuery -->
<script
  src="https://code.jquery.com/jquery-3.6.0.min.js"
  integrity="sha512-894YE6QWD5I59HgZOGReFYm4dnWc1Qt5NtvYSaNcOP+u1T9qYdvdihz0PPSiiqn/+/3e7Jo4EaG7TubfWGUrMQ=="
  crossorigin="anonymous"
></script>

<!-- JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.js"></script>
```

## 基本設定

```html
<div class="your-class">
  <div>your content</div>
  <div>your content</div>
  <div>your content</div>
</div>

<script>
  $(document).ready(function () {
    $('.your-class').slick()
  })
</script>
```

也可以用 `ul > li` 排列，輪播設定以 JS 為主

## DEMO

點擊左側照片，可以控制右側畫面所呈現的照片，同時左側照片也會隨著照片點擊方向，往上或往下滑動一張照片

```javascript
// 右側主要照片
$('.slider-for').slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false,
  fade: true,
  asNavFor: '.slider-nav',
})

// 左側點擊控制照片輪播
$('.slider-nav').slick({
  slidesToShow: 5,
  slidesToScroll: 1,
  asNavFor: '.slider-for',
  dots: false,
  centerMode: true,
  focusOnSelect: true,
  vertical: true,
})
```

## 幾個常用到的設定

### slidesToShow: 1

呈現出來的照片數

### slidesToScroll: 1

滑動一次的照片數，點擊左右的箭頭，一次會滑動的數量。若 **slidesToShow** 和 **slidesToScroll** 數字一樣，點一次滑動整排投影片都換一輪

### asNavFor

讓投影片互相輪動，後面加入選擇器，型別字串

### arrows

箭頭是否呈現，預設 `true`

### fade

淡入淡出，預設 `false`

### dots

現在輪到第幾個的點，預設 `true`

### centerMode

預設 `false`，讓前一張和後一張投影片不會出現，使用於 `slidesToShow` 是奇數時候。

設定 `true`，投影片會像 demo 所示，前一張與後一張出現一部分，但不是整張圖片。若沒有設定 `centerPadding`，預設是出現 50px

### centerPadding

預設 50px，型別字串。設定為 center mode 時，可設定 padding 值（px 或 %）

### vertical

boolean，投影片為垂直，預設 `false`

### zIndex

預設值 1000

### responsive

響應式斷點設定，也可一併在 JS 中設定。值為陣列包物件，`breakpoint` 為斷點 pixel 值，`settings` 內加入各斷點設定，取消 slider 效果用 `settings: "unslick"`

```javascript
responsive: [
  {
    breakpoint: 1024,
    settings: {
      // ...
    },
  },
  {
    breakpoint: 600,
    settings: {
      // ...
    },
  },
  {
    breakpoint: 480,
    settings: 'unslick',
  },
]
```

## 事件

```javascript
// On swipe event
$('.your-element').on('swipe', function (event, slick, direction) {
  console.log(direction) // left
})

// On edge hit
$('.your-element').on('edge', function (event, slick, direction) {
  console.log('edge was hit')
})

// On before slide change
$('.your-element').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
  console.log(nextSlide)
})
```
