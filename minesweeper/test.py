from requests import put, get


def print_board(res):
    data = res.json()
    for row in data["cells"]:
        row = [str(col["proximity"]) if col["proximity"] is not None else "_"
               for col in row]
        print(" ".join(row))


if __name__ == '__main__':
    print("creating new game")
    res = put("http://localhost:5000/games/1",
              data={"rows": 20, "cols": 20, "mines": 20})

    print("getting game 1")
    res = get("http://localhost:5000/games/1")
    print_board(res)

    print("clicking cell 0 0")
    res = put("http://localhost:5000/cells/1/0/0", data={"action": "click"})
    print_board(res)

    print("clicking cell 5 5")
    res = put("http://localhost:5000/cells/1/5/5", data={"action": "click"})
    print_board(res)

