CREATE TABLE IF NOT EXISTS airbnb.airbnblistings (
    host_id int,
    id int,
    availability_365 int,
    calculated_host_listings_count int,
    host_name text,
    latitude float,
    longitude float,
    minimum_nights int,
    neighbourhood text,
    number_of_reviews int,
    price int,
    room_type text,
    PRIMARY KEY (host_id, id)
) WITH ID = e0b76de0-904a-11ec-acd3-8fd66868d933
    AND CLUSTERING ORDER BY (id ASC)
    AND additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND cdc = false
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND extensions = {}
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';
