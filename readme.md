# Wireguard lite monitoring


## sqlite3.37 on Ubuntu
```shell
cd ~ ;\
wget https://github.com/nalgeon/sqlite/releases/download/3.38.0/sqlite3-ubuntu ;\
mv sqlite3-ubuntu sqlite3 ;\
chmod +x sqlite3

# run
~/sqlite3 -box
```

## Run
```shell
python main.py
```

## Check stats
```shell
~/sqlite3 $HOME/db/wg-stats.db -box
```
```sql
select * from v_stats;
```