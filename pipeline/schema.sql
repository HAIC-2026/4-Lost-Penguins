CREATE TABLE sources (
    source_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    retrieved_at TEXT NOT NULL
);

CREATE TABLE metrics (
    metric_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    unit TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_table TEXT, --could be used for source thats not ACS and wont need a table id maybe
    alias TEXT,
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE facts (
    area_id TEXT NOT NULL,
    metric_id TEXT NOT NULL,
    value REAL, 
    moe REAL,
    source_id TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (metric_id) REFERENCES metrics(metric_id),
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    PRIMARY KEY (area_id, metric_id)
);

