import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import (
    Astronaut,
    Spacecraft,
    Mission,
)
from django.db.models import (
    Q,
    F,
    Count,
    Avg,
)

# Create queries within functions

# Django queries I

def get_astronauts(search_string=None):
    """
    SELECT
        astronaut.*,
    FROM astronaut
    WHERE name ILIKE "%search_string%"
        OR phone_number ILIKE "%search_string%"
    ORDER BY
        name ASC;
    """

    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains = search_string) |
        Q(phone_number__icontains = search_string)
    )

    astronauts = astronauts.order_by('name')

    if not astronauts.exists():
        return ""

    return "\n".join(f"Astronaut: {a.name}, "
                    f"phone number: {a.phone_number}, "
                    f"status: {'Active' if a.is_active else 'Inactive'}"
                    for a in astronauts)

def get_top_astronaut():
    """
    SELECT
        astronaut.*,
        COUNT(mission_astronaut.mission_id) AS num_of_missions
    FROM astronaut
    LEFT JOIN mission_astronaut
        ON astronaut.id = mission_astronaut.astronaut_id
    GROUP BY
        astronaut.id
    ORDER BY
        num_of_missions DESC,
        phone_number ASC
    LIMIT 1;
    """

    astronaut = Astronaut.objects.get_astronauts_by_missions_count().first()

    if not astronaut or astronaut.missions_count == 0:
        return "No data."

    return f"Top Astronaut: {astronaut.name} with {astronaut.missions_count} missions."

def get_top_commander():
    """
    SELECT
        astronaut.*,
        COUNT(mission.id) AS num_of_missions
    FROM astronaut
    LEFT JOIN mission
        ON astronaut.id = mission.commander_id
    GROUP BY
        astronaut.id
    ORDER BY
        num_of_missions DESC,
        phone_number ASC
    LIMIT 1;
    """

    astronaut = Astronaut.objects.annotate(
        commanded_missions_count = Count('commanded_missions')
    ).order_by(
        '-commanded_missions_count',
        'phone_number',
    ).first()

    if not astronaut or astronaut.commanded_missions_count == 0:
        return "No data."

    return f"Top Commander: {astronaut.name} with {astronaut.commanded_missions_count} commanded missions."

# Django queries II

def get_last_completed_mission():
    """
    SELECT
        mission.*
    FROM mission
    WHERE
        status = 'Completed'
    ORDER BY
        launch_date DESC
    LIMIT 1;
    """

    mission = (
        Mission.objects.filter(
            status="Completed"
        ).select_related(
            "commander",
            "spacecraft"
        ).prefetch_related(
            "astronauts"
        ).order_by(
            "-launch_date"
        ).first()
    )

    if not mission:
        return "No data."

    astronauts = list(mission.astronauts.order_by('name'))

    commander = mission.commander.name if mission.commander and mission.commander.name else "TBA"

    astronaut_names = ", ".join(a.name for a in astronauts)

    spacecraft = mission.spacecraft.name

    sum_spacewalks = sum(a.spacewalks for a in astronauts)

    return (
        f"The last completed mission is: {mission.name}. "
        f"Commander: {commander}. "
        f"Astronauts: {astronaut_names}. "
        f"Spacecraft: {spacecraft}. "
        f"Total spacewalks: {sum_spacewalks}."
    )

def get_most_used_spacecraft():
    """
    SELECT
        spacecraft.*
        COUNT(mission.spacecraft_id) AS count_missions
    FROM spacecraft
    LEFT JOIN mission
    ORDER BY
        name ASC
    LIMIT 1;
    """

    spacecraft = Spacecraft.objects.annotate(
        count_missions = Count('missions', distinct=True),
        count_astronauts = Count('missions__astronauts', distinct=True)
    ).order_by(
        '-count_missions',
        'name'
    ).first()

    if not spacecraft or spacecraft.count_missions == 0:
        return 'No data.'

    return (
        f"The most used spacecraft is: {spacecraft.name}, "
        f"manufactured by {spacecraft.manufacturer}, "
        f"used in {spacecraft.count_missions} missions, "
        f"astronauts on missions: {spacecraft.count_astronauts}."
    )

def decrease_spacecrafts_weight():
    """
    SELECT DISTINCT
        spacecraft.*
    FROM spacecraft
    JOIN mission
        ON spacecraft.id = mission.spacecraft_id
    WHERE
        mission.status = 'Planned'
        AND spacecraft.weight >= 200;

    UPDATE spacecraft
    SET weight = weight - 200
    WHERE id IN (
        SELECT DISTINCT spacecraft.id
        FROM spacecraft
        JOIN mission
            ON spacecraft.id = mission.spacecraft_id
        WHERE
            mission.status = 'Planned'
            AND spacecraft.weight >= 200
    );
    """

    spacecrafts = Spacecraft.objects.filter(
        missions__status = 'Planned',
        weight__gte = 200
    ).distinct()

    count = spacecrafts.count()

    if count == 0:
        return 'No changes in weight.'

    spacecrafts.update(
        weight = F('weight') - 200
    )

    avg_weight = Spacecraft.objects.aggregate(
        avg = Avg('weight')
    )['avg']

    return (
        f"The weight of {count} spacecrafts has been decreased. "
        f"The new average weight of all spacecrafts is {avg_weight:.1f}kg"
    )

# # Creating astronauts

# def populate_db():

#     astronaut1 = Astronaut.objects.create(
#         name = 'John Deer',
#         phone_number = '853967',
#         is_active = True,
#         date_of_birth = '1980-01-01',
#         spacewalks = 3,
#     )

#     astronaut2 = Astronaut.objects.create(
#         name = 'Jane Smith',
#         phone_number = '123456',
#         is_active = True,
#         date_of_birth = '1985-05-15',
#         spacewalks = 1,
#     )

#     astronaut3 = Astronaut.objects.create(
#         name = 'Josie Stam',
#         phone_number = '111111',
#         is_active = False,
#         date_of_birth = '1990-03-12',
#         spacewalks = 0,
#     )

#     # Creating spacecrafts

#     spacecraft1 = Spacecraft.objects.create(
#         name = 'Explorer I',
#         manufacturer = 'SpaceTech Inc.',
#         capacity = 5,
#         weight = 12000.5,
#         launch_date = '2022-01-01',
#     )

#     spacecraft2 = Spacecraft.objects.create(
#         name = 'Explorer II',
#         manufacturer = 'SpaceX',
#         capacity = 2,
#         weight = 10000.2,
#         launch_date = '2023-05-01',
#     )

#     # Creating missions

#     mission1 = Mission.objects.create(
#         name = 'Moon Landing',
#         description = "It's aimed at landing on the moon",
#         status = 'Planned',
#         launch_date = '2024-10-10',
#         spacecraft = spacecraft1,
#         commander = astronaut1,
#     )
#     mission1.astronauts.add(astronaut1, astronaut2)

#     mission2 = Mission.objects.create(
#         name = 'Moon Landing2',
#         description = "It's also aimed at landing on the moon",
#         status = 'Completed',
#         launch_date = '2024-03-01',
#         spacecraft = spacecraft1,
#         commander = astronaut3,
#     )
#     mission2.astronauts.add(astronaut2, astronaut3)

# populate_db()

# print(Astronaut.objects.get_astronauts_by_missions_count())
# print('===========================================================================================')
# print(get_astronauts(search_string='jO'))
# print('===========================================================================================')
# print(get_astronauts(search_string='zzz'))
# print('===========================================================================================')
# print(get_top_astronaut())
# print('===========================================================================================')
# print(get_top_commander())
# print('===========================================================================================')
# print(get_last_completed_mission())
# print('===========================================================================================')
# print(get_most_used_spacecraft())
# print('===========================================================================================')
# print(decrease_spacecrafts_weight())
# print('===========================================================================================')
