# 記帳軟體系統 — 流程圖文件

> **版本**：v1.0  
> **建立日期**：2026-04-23  
> **對應文件**：docs/PRD.md、docs/ARCHITECTURE.md  

---

## 1. 使用者流程圖（User Flow）

### 1.1 整體操作流程

使用者進入網站後，可在首頁查看餘額統計與近期交易，並從導覽列進入各功能模組。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B["首頁 - 餘額統計 + 近期交易"]

    B --> C{要執行什麼操作？}

    C -->|新增交易| D["新增交易表單頁"]
    C -->|查看所有交易| E["交易列表頁"]
    C -->|分析報表| F["分析報表頁"]
    C -->|管理類別| G["類別管理頁"]

    D --> D1["填寫金額、類型、類別、日期、備註"]
    D1 --> D2{表單驗證}
    D2 -->|通過| D3["儲存成功，重導回首頁"]
    D2 -->|失敗| D4["顯示錯誤訊息"]
    D4 --> D1
    D3 --> B

    E --> E1{要執行什麼操作？}
    E1 -->|篩選搜尋| E2["設定篩選條件"]
    E2 --> E3["顯示篩選結果"]
    E1 -->|編輯| E4["編輯交易表單頁"]
    E4 --> E5["修改資料並送出"]
    E5 --> E6{表單驗證}
    E6 -->|通過| E7["更新成功，重導回列表"]
    E6 -->|失敗| E8["顯示錯誤訊息"]
    E8 --> E4
    E7 --> E
    E1 -->|刪除| E9["確認刪除對話"]
    E9 -->|確認| E10["刪除成功，重導回列表"]
    E9 -->|取消| E
    E10 --> E

    F --> F1{查看哪種報表？}
    F1 -->|圓餅圖| F2["選擇月份"]
    F2 --> F3["顯示收支佔比圓餅圖 + 明細"]
    F1 -->|月度摘要| F4["顯示各月收支摘要表"]

    G --> G1{要執行什麼操作？}
    G1 -->|新增類別| G2["填寫類別名稱與類型"]
    G2 --> G3["儲存成功"]
    G3 --> G
    G1 -->|編輯類別| G4["修改類別名稱"]
    G4 --> G
    G1 -->|刪除類別| G5["確認刪除"]
    G5 --> G
```

### 1.2 新增交易流程（詳細版）

```mermaid
flowchart LR
    A([使用者點擊「新增交易」]) --> B["進入表單頁面"]
    B --> C["選擇類型：收入 / 支出"]
    C --> D["選擇類別"]
    D --> E["輸入金額"]
    E --> F["選擇日期"]
    F --> G["輸入備註（選填）"]
    G --> H["點擊送出"]
    H --> I{伺服器驗證}
    I -->|金額為正數 ✓| J["寫入資料庫"]
    I -->|驗證失敗 ✗| K["返回表單，顯示錯誤"]
    K --> C
    J --> L["重導向至首頁"]
    L --> M["首頁餘額即時更新"]
```

### 1.3 搜尋與篩選流程

```mermaid
flowchart LR
    A([使用者進入交易列表]) --> B["顯示所有交易紀錄"]
    B --> C{選擇篩選方式}
    C -->|日期範圍| D["選擇起始與結束日期"]
    C -->|類別| E["從下拉選單選擇類別"]
    C -->|類型| F["選擇收入或支出"]
    C -->|關鍵字| G["輸入備註關鍵字"]
    D --> H["送出篩選條件"]
    E --> H
    F --> H
    G --> H
    H --> I["顯示篩選後的交易紀錄"]
    I --> J{繼續操作？}
    J -->|調整篩選| C
    J -->|清除篩選| B
    J -->|編輯某筆| K["進入編輯頁面"]
    J -->|刪除某筆| L["確認刪除"]
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增交易紀錄

描述使用者從「點擊新增」到「資料存入資料庫」的完整流程：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br>transaction.py
    participant Model as Model<br>Transaction
    participant DB as SQLite

    User->>Browser: 點擊「新增交易」按鈕
    Browser->>Route: GET /transaction/new
    Route->>Model: 查詢所有類別（供表單選擇）
    Model->>DB: SELECT * FROM categories
    DB-->>Model: 類別列表
    Model-->>Route: 類別資料
    Route-->>Browser: 渲染 form.html（含類別下拉選單）
    Browser-->>User: 顯示新增交易表單

    User->>Browser: 填寫表單並點擊送出
    Browser->>Route: POST /transaction/new
    Route->>Route: 驗證表單資料（金額 > 0、日期格式等）

    alt 驗證通過
        Route->>Model: 建立 Transaction 物件
        Model->>DB: INSERT INTO transactions
        DB-->>Model: 儲存成功
        Model-->>Route: 回傳新紀錄
        Route-->>Browser: 302 Redirect 至首頁
        Browser-->>User: 顯示首頁（餘額已更新）
    else 驗證失敗
        Route-->>Browser: 渲染 form.html（含錯誤訊息）
        Browser-->>User: 顯示錯誤提示
    end
```

### 2.2 編輯交易紀錄

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br>transaction.py
    participant Model as Model<br>Transaction
    participant DB as SQLite

    User->>Browser: 點擊某筆交易的「編輯」按鈕
    Browser->>Route: GET /transaction/3/edit
    Route->>Model: 查詢 Transaction id=3
    Model->>DB: SELECT * FROM transactions WHERE id=3
    DB-->>Model: 交易資料
    Route->>Model: 查詢所有類別
    Model->>DB: SELECT * FROM categories
    DB-->>Model: 類別列表
    Model-->>Route: 交易 + 類別資料
    Route-->>Browser: 渲染 form.html（帶入現有資料）
    Browser-->>User: 顯示已填入的編輯表單

    User->>Browser: 修改資料並點擊送出
    Browser->>Route: POST /transaction/3/edit

    alt 驗證通過
        Route->>Model: 更新 Transaction 物件
        Model->>DB: UPDATE transactions SET ... WHERE id=3
        DB-->>Model: 更新成功
        Route-->>Browser: 302 Redirect 至交易列表
        Browser-->>User: 顯示更新後的交易列表
    else 驗證失敗
        Route-->>Browser: 渲染 form.html（含錯誤訊息）
        Browser-->>User: 顯示錯誤提示
    end
```

### 2.3 刪除交易紀錄

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br>transaction.py
    participant Model as Model<br>Transaction
    participant DB as SQLite

    User->>Browser: 點擊某筆交易的「刪除」按鈕
    Browser->>Route: POST /transaction/3/delete
    Route->>Model: 查詢 Transaction id=3
    Model->>DB: SELECT * FROM transactions WHERE id=3
    DB-->>Model: 交易資料

    alt 紀錄存在
        Route->>Model: 刪除 Transaction
        Model->>DB: DELETE FROM transactions WHERE id=3
        DB-->>Model: 刪除成功
        Route-->>Browser: 302 Redirect 至交易列表
        Browser-->>User: 顯示更新後的列表（已移除該筆）
    else 紀錄不存在
        Route-->>Browser: 404 Not Found
        Browser-->>User: 顯示錯誤頁面
    end
```

### 2.4 圓餅圖分析

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br>analysis.py
    participant Model as Model<br>Transaction
    participant DB as SQLite
    participant Chart as Chart.js

    User->>Browser: 點擊「分析報表」並選擇月份
    Browser->>Route: GET /analysis?month=2026-04
    Route->>Model: 查詢該月所有交易
    Model->>DB: SELECT category_id, SUM(amount)<br>FROM transactions<br>WHERE date BETWEEN ... AND ...<br>GROUP BY category_id
    DB-->>Model: 各類別加總資料
    Model-->>Route: 彙整後的統計資料
    Route-->>Browser: 渲染 charts.html（含圖表資料）
    Browser->>Chart: 初始化圓餅圖（傳入 JSON 資料）
    Chart-->>Browser: 繪製圓餅圖
    Browser-->>User: 顯示收支佔比圓餅圖 + 明細表
```

### 2.5 月度收支摘要

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route<br>analysis.py
    participant Model as Model<br>Transaction
    participant DB as SQLite

    User->>Browser: 點擊「月度摘要」
    Browser->>Route: GET /analysis/summary
    Route->>Model: 查詢近 12 個月的收支統計
    Model->>DB: SELECT strftime('%Y-%m', date) as month,<br>type, SUM(amount)<br>FROM transactions<br>GROUP BY month, type
    DB-->>Model: 各月收支彙總
    Model-->>Route: 整理為月度摘要列表
    Route-->>Browser: 渲染 summary.html
    Browser-->>User: 顯示月度收支摘要表<br>（含盈餘/赤字顏色標示）
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|---------|-----------|------|
| 首頁總覽 | `/` | GET | 顯示餘額統計與近期交易紀錄 |
| 新增交易（表單） | `/transaction/new` | GET | 顯示新增交易表單 |
| 新增交易（送出） | `/transaction/new` | POST | 驗證並儲存新交易紀錄 |
| 交易列表 | `/transactions` | GET | 顯示所有交易，支援篩選與搜尋 |
| 編輯交易（表單） | `/transaction/<id>/edit` | GET | 顯示編輯交易表單（帶入現有資料） |
| 編輯交易（送出） | `/transaction/<id>/edit` | POST | 驗證並更新交易紀錄 |
| 刪除交易 | `/transaction/<id>/delete` | POST | 刪除指定交易紀錄 |
| 圓餅圖分析 | `/analysis` | GET | 顯示月度各類別收支佔比圓餅圖 |
| 月度摘要 | `/analysis/summary` | GET | 顯示近 12 個月收支摘要表 |
| 類別列表 | `/categories` | GET | 顯示所有收支類別 |
| 新增類別（表單） | `/categories/new` | GET | 顯示新增類別表單 |
| 新增類別（送出） | `/categories/new` | POST | 儲存新類別 |
| 編輯類別（表單） | `/categories/<id>/edit` | GET | 顯示編輯類別表單 |
| 編輯類別（送出） | `/categories/<id>/edit` | POST | 更新類別資料 |
| 刪除類別 | `/categories/<id>/delete` | POST | 刪除指定類別 |

---

## 附錄：頁面導覽關係圖

```mermaid
flowchart TB
    NAV["🧭 導覽列（所有頁面共用）"]

    NAV --> HOME["🏠 首頁<br>/"]
    NAV --> LIST["📋 交易列表<br>/transactions"]
    NAV --> NEW["➕ 新增交易<br>/transaction/new"]
    NAV --> ANALYSIS["📊 分析報表<br>/analysis"]
    NAV --> CAT["🏷️ 類別管理<br>/categories"]

    HOME -->|"點擊交易紀錄"| EDIT["✏️ 編輯交易<br>/transaction/id/edit"]
    LIST -->|"點擊編輯"| EDIT
    LIST -->|"點擊刪除"| DEL["🗑️ 刪除交易<br>/transaction/id/delete"]

    ANALYSIS --> CHART["🥧 圓餅圖<br>/analysis"]
    ANALYSIS --> SUMMARY["📅 月度摘要<br>/analysis/summary"]

    CAT -->|"點擊新增"| CATNEW["➕ 新增類別<br>/categories/new"]
    CAT -->|"點擊編輯"| CATEDIT["✏️ 編輯類別<br>/categories/id/edit"]
    CAT -->|"點擊刪除"| CATDEL["🗑️ 刪除類別<br>/categories/id/delete"]

    NEW -->|"送出成功"| HOME
    EDIT -->|"送出成功"| LIST
    DEL -->|"刪除成功"| LIST
    CATNEW -->|"送出成功"| CAT
    CATEDIT -->|"送出成功"| CAT
    CATDEL -->|"刪除成功"| CAT
```
