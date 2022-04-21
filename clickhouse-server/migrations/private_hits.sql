CREATE TABLE default.private_hits (
    added           DateTime MATERIALIZED now(),
    idfa            String,
    idfv            String,
    advertising_id  LowCardinality(String),
    android_id      String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(added)
ORDER BY(added, idfa, advertising_id);
