from requests import put, get, post


def print_board(res):
    data = res.json()
    for row in data["cells"]:
        row = [str(col["proximity"]) if col["proximity"] is not None else "_"
               for col in row]
        print(" ".join(row))


if __name__ == '__main__':
    print("creating new game")
    res = post("http://localhost:5000/games",
              data={"rows": 20, "cols": 20, "mines": 20})

    board_data = res.json()
    game_id = board_data["game_id"]
    print("getting game")
    res = get("http://localhost:5000/games/{}".format(game_id))
    print_board(res)

    print("clicking cell 0 0")
    res = put("http://localhost:5000/cells/{}/0/0".format(game_id), json={"action": "click"})
    print_board(res)

    print("clicking cell 5 5")
    res = put("http://localhost:5000/cells/{}/5/5".format(game_id), json={"action": "click"})
    print_board(res)

