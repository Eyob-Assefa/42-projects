import random
import typing


def gen_event() -> typing.Generator[tuple[str, str], None, None]:
    players: list[str] = ["bob", "alice", "dylan", "charlie"]
    actions: list[str] = ["run", "eat", "sleep", "grab", "move", "climb",
                          "swim", "use", "release"]

    while True:
        p: str = random.choice(players)
        a: str = random.choice(actions)
        yield (p, a)


def consume_event(
                    events: list[tuple[str, str]]
                 ) -> typing.Generator[tuple[str, str], None, None]:

    while len(events) > 0:
        idx: int = random.randint(0, len(events) - 1)
        evt: tuple[str, str] = events[idx]
        del events[idx]
        yield evt


def ft_data_stream() -> None:
    print("=== Game Data Stream Processor ===")

    stream: typing.Generator[tuple[str, str], None, None] = gen_event()

    i: int
    for i in range(1000):
        evt: tuple[str, str] = next(stream)
        print(f"Event {i}: Player {evt[0]} did action {evt[1]}")

    ten_events: list[tuple[str, str]] = []

    j: int
    for j in range(10):
        ten_events.append(next(stream))

    print(f"Built list of 10 events: {ten_events}")

    consumer: typing.Generator[
        tuple[str, str], None, None
    ] = consume_event(ten_events)

    c_evt: tuple[str, str]
    for c_evt in consumer:
        print(f"Got event from list: {c_evt}")
        print(f"Remains in list: {ten_events}")


if __name__ == "__main__":
    ft_data_stream()
