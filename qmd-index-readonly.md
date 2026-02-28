# QMD Index Readonly Snapshot

- Generated: 2026-02-28T21:45:22
- DB: `/mnt/e/Openclaw/.openclaw/agents/main/qmd/xdg-cache/qmd/index.sqlite`

## Tables
- `content`
- `content_vectors`
- `documents`
- `documents_fts`
- `documents_fts_config`
- `documents_fts_content`
- `documents_fts_data`
- `documents_fts_docsize`
- `documents_fts_idx`
- `llm_cache`
- `sqlite_sequence`
- `vectors_vec`
- `vectors_vec_chunks`
- `vectors_vec_info`
- `vectors_vec_rowids`
- `vectors_vec_vector_chunks00`

## Schema: `documents`
```sql
CREATE TABLE documents (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      collection TEXT NOT NULL,
      path TEXT NOT NULL,
      title TEXT NOT NULL,
      hash TEXT NOT NULL,
      created_at TEXT NOT NULL,
      modified_at TEXT NOT NULL,
      active INTEGER NOT NULL DEFAULT 1,
      FOREIGN KEY (hash) REFERENCES content(hash) ON DELETE CASCADE,
      UNIQUE(collection, path)
    )
```

## Schema: `content`
```sql
CREATE TABLE content (
      hash TEXT PRIMARY KEY,
      doc TEXT NOT NULL,
      created_at TEXT NOT NULL
    )
```

## Schema: `content_vectors`
```sql
CREATE TABLE content_vectors (
      hash TEXT NOT NULL,
      seq INTEGER NOT NULL DEFAULT 0,
      pos INTEGER NOT NULL DEFAULT 0,
      model TEXT NOT NULL,
      embedded_at TEXT NOT NULL,
      PRIMARY KEY (hash, seq)
    )
```

## Sample rows: documents

| id | collection | path | title | active |
|---:|---|---|---|---:|
| 21 | memory-root-main | memory.md | MEMORY | 1 |
| 22 | memory-alt-main | memory.md | MEMORY | 1 |
| 23 | memory-dir-main | 2026-02-28.md | 2026-02-28 | 1 |
