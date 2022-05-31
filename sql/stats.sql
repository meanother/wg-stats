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