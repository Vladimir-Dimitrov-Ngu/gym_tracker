from database.operations import add_custom_equipment, get_equipment_description


def add_initial_equipment():
    equipment_data = {
        'Bench Press': ('Chest', 'A weight training bench with a barbell for chest exercises.'),
        'Incline Bench Press': ('Chest', 'An angled bench for targeting upper chest muscles.'),
        'Chest Fly Machine': ('Chest', 'A machine that simulates a dumbbell fly motion for chest isolation.'),
        'Squat Rack': ('Legs', 'A sturdy frame for performing barbell squats and other leg exercises.'),
        'Leg Press Machine': ('Legs', 'A machine where you push a weight platform with your legs.'),
        'Leg Extension Machine': ('Legs', 'A machine for isolating and strengthening the quadriceps.'),
        'Lat Pulldown Machine': ('Back', 'A cable machine for performing lat pulldowns to target the back muscles.'),
        'Seated Cable Row': ('Back', 'A machine for performing seated rows to work the middle back.'),
        'T-Bar Row Machine': ('Back', 'A machine that allows for t-bar rows to target the upper and middle back.')
    }
    
    for name, (muscle_group, description) in equipment_data.items():
        existing_description = get_equipment_description(name)
        if existing_description is None:
            add_custom_equipment(name, muscle_group, description)
        else:
            print(f"Equipment '{name}' already exists. Skipping.")