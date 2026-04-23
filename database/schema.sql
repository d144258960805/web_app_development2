-- ============================================
-- 記帳軟體系統 — SQLite 資料庫 Schema
-- 版本：v1.0
-- 建立日期：2026-04-23
-- ============================================

-- 啟用外鍵約束（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- --------------------------------------------
-- 1. 收支類別表（categories）
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(50) NOT NULL,
    type        VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- 同類型下不可有重複名稱
    UNIQUE(name, type)
);

-- 索引：依類別類型篩選
CREATE INDEX IF NOT EXISTS idx_categories_type ON categories(type);

-- --------------------------------------------
-- 2. 交易紀錄表（transactions）
-- --------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    amount      REAL        NOT NULL CHECK (amount > 0),
    type        VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    category_id INTEGER     NOT NULL,
    date        DATE        NOT NULL,
    note        TEXT        NOT NULL DEFAULT '',
    created_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- 外鍵約束：關聯至 categories 表
    FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 索引：加速常用查詢
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_category_id ON transactions(category_id);

-- --------------------------------------------
-- 3. 預設類別資料（Seed Data）
-- --------------------------------------------

-- 支出類別
INSERT OR IGNORE INTO categories (name, type) VALUES ('餐飲', 'expense');
INSERT OR IGNORE INTO categories (name, type) VALUES ('交通', 'expense');
INSERT OR IGNORE INTO categories (name, type) VALUES ('娛樂', 'expense');
INSERT OR IGNORE INTO categories (name, type) VALUES ('購物', 'expense');
INSERT OR IGNORE INTO categories (name, type) VALUES ('住宿', 'expense');
INSERT OR IGNORE INTO categories (name, type) VALUES ('醫療', 'expense');
INSERT OR IGNORE INTO categories (name, type) VALUES ('教育', 'expense');
INSERT OR IGNORE INTO categories (name, type) VALUES ('其他支出', 'expense');

-- 收入類別
INSERT OR IGNORE INTO categories (name, type) VALUES ('薪水', 'income');
INSERT OR IGNORE INTO categories (name, type) VALUES ('獎學金', 'income');
INSERT OR IGNORE INTO categories (name, type) VALUES ('打工', 'income');
INSERT OR IGNORE INTO categories (name, type) VALUES ('零用錢', 'income');
INSERT OR IGNORE INTO categories (name, type) VALUES ('投資', 'income');
INSERT OR IGNORE INTO categories (name, type) VALUES ('其他收入', 'income');
