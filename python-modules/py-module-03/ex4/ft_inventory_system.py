import sys


def ft_inventory_system() -> None:
    print("=== Inventory System Analysis ===")

    inv: dict[str, int] = {}

    arg: str
    for arg in sys.argv[1:]:
        parts: list[str] = arg.split(":")

        if len(parts) != 2:
            print(f"Error invalid parameter '{arg}'")
            continue

        name: str = parts[0]
        val_str: str = parts[1]

        if name in inv.keys():
            print(f"Redundant item '{name}' discarding")
            continue

        try:
            qty: int = int(val_str)
            inv.update({name: qty})
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")

    print(f"Got inventory: {inv}")

    item_list: list[str] = list(inv.keys())
    print(f"Item list: {item_list}")

    vals: list[int] = list(inv.values())
    total: int = sum(vals)
    inv_len: int = len(inv)
    print(f"Total quantity of the {inv_len} items: {total}")

    item_name: str
    for item_name in item_list:
        pct: float = round((inv[item_name] / total) * 100, 1)
        print(f"Item {item_name} represents {pct}%")

    most_name: str = ""
    most_qty: int = -1
    least_name: str = ""
    least_qty: int = -1

    n: str
    for n in item_list:
        curr_qty: int = inv[n]
        if most_qty == -1 or curr_qty > most_qty:
            most_qty = curr_qty
            most_name = n
        if least_qty == -1 or curr_qty < least_qty:
            least_qty = curr_qty
            least_name = n

    print(f"Item most abundant: {most_name} with quantity {most_qty}")
    print(f"Item least abundant: {least_name} with quantity {least_qty}")

    # Changed to bound method: inv.update()
    inv.update({'magic_item': 1})
    print(f"Updated inventory: {inv}")


if __name__ == "__main__":
    ft_inventory_system()
