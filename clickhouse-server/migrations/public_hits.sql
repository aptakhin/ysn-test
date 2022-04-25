CREATE TABLE default.public_hits (
    added     DateTime MATERIALIZED now(),
    json_data String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(added)
ORDER BY(added);
