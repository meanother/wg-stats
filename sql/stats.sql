create table IF NOT EXISTS stats(
    id integer primary key AUTOINCREMENT,
    interface text null,
    peers text null,
    preshared_keys text null,
    endpoints text null,
    ip_address text null,
    allowed_ips text null,
    latest_handshakes text null,
    transfer_receiver real null,
    transfer_sender real null,
    persistent_keepalive text null,
    event_ts timestamp not null
);

create table IF NOT EXISTS wg0_users(
    id integer primary key AUTOINCREMENT,
    peer_key text null,
    peer_ip text null,
    event_ts timestamp not null
);

create table IF NOT EXISTS user_map(
    id integer primary key AUTOINCREMENT,
    username text null,
    key text null,
    event_ts timestamp not null
);

create view v_stats as
with user_map_ as
(
    select *, row_number() over(partition by username order by event_ts desc) as row_n from user_map
),
stats_ as
(
    select *, row_number() over(partition by peers order by event_ts desc) as row_n from stats
)
select
    u.username
    , s.interface
    , s.ip_address
    , s.allowed_ips
    , s.latest_handshakes
    , s.transfer_receiver as transfer_out_gb
    , s.transfer_sender   as transfer_in_gb
from
    user_map_ u
    left join stats_ s
        on u.key = s.peers
        and s.row_n = 1
where
    u.row_n = 1;