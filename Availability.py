import random
from tabulate import tabulate

#generate random available times for each person
def generate_availability(num_people):
    availability = {}
    for person in range(1, num_people + 1):
        available_times = []
        for _ in range(random.randint(1, 5)):  # Randomly generates available times per person
            start_time = random.randint(0, 23)  # Random start hour for the available time frame
            end_time = random.randint(start_time + 1, 24)  # Random end hour after start hour marking end of the available time
            available_times.append((start_time, end_time))
        availability[f"Person {person}"] = available_times
    return availability

def convert_to_ampm(hour): # convert 24-hour format to AM/PM
    if hour == 0:
        return "12 AM"
    elif hour < 12:
        return f"{hour} AM"
    elif hour == 12:
        return "12 PM"
    else:
        return f"{hour - 12} PM"

num_people = int(input("Enter the number of people: "))


availability = generate_availability(num_people)


availability_table = {} # Initialzing table
for hour in range(24):
    time_slot = convert_to_ampm(hour)
    availability_table[time_slot] = [''] * num_people

time_slots = list(availability_table.keys())


for person, times in availability.items(): #filling table
    for start, end in times:
        for hour in range(start, end):
            time_slot = convert_to_ampm(hour)
            person_index = int(person.split()[1]) - 1
            availability_table[time_slot][person_index] = 'X'


table_data = []
for time_slot in time_slots:
    row = [time_slot] + availability_table[time_slot]
    table_data.append(row)


# Print availability table
print("\nAvailability:")
print(tabulate(table_data, headers=["Time"] + [f"Person {i+1}" for i in range(num_people)]))

# Count the number of available people for each time slot
available_counts = {}
for time_slot in time_slots:
    count = 0
    for person_available in availability_table[time_slot]:
      if person_available == 'X':
        count += 1
    available_counts[time_slot] = count

# Find the time slot with the maximum number of available people
max_available_slot = max(available_counts, key=available_counts.get)

# Print the suggested time slot
print(f"\nSuggested Time Slot: {max_available_slot} (Majority of {available_counts[max_available_slot]} people available)")
