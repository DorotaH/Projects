from .models import inhabitants


def generate_bearers(inputPoints):
    people = []
    pairs = []
    for i in range(inputPoints):
        id = i
        people.append(inhabitants(id))

    matching_personality_direction = {}
    # tworzymy dwa slowniki dla direction 0 i 1
    matching_personality_direction[0] = {0: [], 1: []}
    matching_personality_direction[1] = {0: [], 1: []}

    # przypisz kazda osobe do odpowiedniego slownika
    for person in people:
        matching_personality_direction[person.personality][
            person.direction
        ].append(person)

    # dla personality 0 i 1 dopasuj osoby o direction 0 i 1
    for j in range(2):
        while (
            matching_personality_direction[j][0]
            and matching_personality_direction[j][1]
        ):
            pairs.append(
                (
                    matching_personality_direction[j][0].pop(),
                    matching_personality_direction[j][1].pop(),
                )
            )
    if pairs == []:
        people = [
            {"id": 0, "personality": 0, "direction": 0, "energy": 27},
            {"id": 1, "personality": 0, "direction": 1, "energy": 18},
        ]
    else:
        pairs = len(pairs)
    return pairs, people
