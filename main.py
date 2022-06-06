from src.preprocess import (
    convert_output,
    get_user_public_id,
    get_users,
    read_wg0,
    run_shell_cmd,
)
from src.utils import insert, create_parser


def main():
    args = create_parser()

    for stat in convert_output(run_shell_cmd("wg show all dump")):
        print(stat)
        insert(table="stats", column_values=stat)

    for user_c in read_wg0():
        print(user_c)
        insert(table="wg0_users", column_values=user_c)

    users_path = args.users_path
    for user_a in get_users(users_path):
        print(user_a)
        insert(table="user_map", column_values=get_user_public_id(users_path, user_a))


if __name__ == "__main__":
    main()
