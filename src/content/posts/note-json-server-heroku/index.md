---
title: '[note] json-server推到heroku遠端 脫離本地端限制'
published: 2021-06-27
description: 'json-server 推到 heroku 遠端，脫離本地端限制，也記錄了自己遇到的坑和排錯過程。'
tags: ['javascript']
author: 'Pei Wang'
draft: false
---

![沒膽站上去的攝影師(我)](https://cdn-images-1.medium.com/max/800/1*ZZdf-KZtVmZOQcnepiVPUg.jpeg)

## 緣由

project 使用 json-server 做簡易 api，為了在之後求職時面試也可以用，將 json 傳到網路上，例如六角學院示範的 heroku，或是 json-server 官方提供的 beta 版 My json server

但推上 heroku 遇到一點困難，可能是 json-server 更新，或是影片是3年前比較舊也有可能。網路上找不到全中文的解法，所以將找到的資源簡單翻譯，並記錄這次排錯過程。

> 分成以下三步驟，若已經建立好 json server，可以直接跳到 2. 準備部屬到 heroku
>
> 1. 建立 api 資料夾
> 2. 部屬到 heroku 前的準備
> 3. 建立 heroku server

## 1. 建立 api 資料夾

假設須建立 fake server 的假 api：

- 建立 fake server 資料夾，建立 node 環境
- 安裝 json server
- 新增 `db.json` 將 api 資料放入

```bash
npm init
npm i json-server
```

- `package.json` 加上並更改 script start 的指令，讓 port 指向 localhost:3004
- `npm start` 啟動 json server

```json
// package.json
{
  "name": "api",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "json-server -p 3004 -w db.json"
  },
  "author": "",
  "license": "ISC"
}
```

到這邊為止，就建立好本地端的 api 囉。此時可以用 postman 測試 `http://localhost:3000` 是否連線成功

> 更改 port 的方式除了上述的更改 package.json，也可以輸入指令
>
> `json-server --watch db.json --port 3004`

## 2. 部屬到 heroku 前的準備

- 修改 `package.json` 的 scripts 中的 start 指令
- main 屬性也改為 `server.js`
- 加上 dependencies

```json
{
  "name": "fake-server",
  "version": "1.0.0",
  "description": "fake server with fake database",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "json-server": "0.16.3"
  }
}
```

- 新增 `server.js`

```javascript
const jsonServer = require('json-server')
const server = jsonServer.create()
const router = jsonServer.router('db.json')
const middlewares = jsonServer.defaults()
const port = process.env.PORT || 3000

server.use(middlewares)
server.use(router)
server.listen(port)
```

## 3. 建立 heroku server

1. 安裝 [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. 登入 heroku

```bash
heroku login
```

3. 在 api 資料夾建立 heroku app

```bash
heroku create
```

4. git 推上 heroku

```bash
git init
git add .
git commit -m "first commit"
git push heroku master
```

5. 開啟 app

```bash
heroku open
```

![](https://cdn-images-1.medium.com/max/800/1*30CA8J6y6S3zSNy44T92Pg.png)

## 遇到的坑

### error: src refspec master does not match any

推上 heroku 時遇到此錯誤，原因是 git 預設分支名稱已改為 `main`

```bash
git push heroku main
```

### Application error

推上去後打開網址出現 Application error，查看 log：

```bash
heroku logs --tail
```

常見原因：`server.js` 中 port 沒有使用 `process.env.PORT`，heroku 會動態分配 port，若寫死會造成錯誤
