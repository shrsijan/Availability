from tabulate import tabulate

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

def convert_to_ampm(hour, minute):
    if hour == 0:
        return f"12:{minute:02d} AM"
    elif hour < 12:
        return f"{hour}:{minute:02d} AM"
    elif hour == 12:
        return f"12:{minute:02d} PM"
    else:
        return f"{hour - 12}:{minute:02d} PM"

def is_morning(hour):
    return 0 <= hour < 12

def is_afternoon(hour):
    return 12 <= hour < 18

def is_evening(hour):
    return 18 <= hour <= 23

availability_list = LinkedList()

# Example availability data for 5 users
availability_data = [
    {"Person": 1, "Availability": [(9, 12), (14, 18)]},
    {"Person": 2, "Availability": [(8, 13), (15, 19)]},
    {"Person": 3, "Availability": [(10, 14), (16, 20)]},
    {"Person": 4, "Availability": [(11, 15), (17, 21)]},
    {"Person": 5, "Availability": [(9, 13), (15, 18)]}
]

for data in availability_data:
    availability_list.insert(data)

availability_table = {}
for hour in range(24):
    for minute in range(0, 60, 15):  # Iterate over 15-minute intervals
        time_slot = convert_to_ampm(hour, minute)
        availability_table[time_slot] = [''] * 5

time_slots = list(availability_table.keys())

current = availability_list.head
while current:
    person = current.data["Person"]
    times = current.data["Availability"]
    for start, end in times:
        for hour in range(start, end):
            for minute in range(0, 60, 15):
                time_slot = convert_to_ampm(hour, minute)
                availability_table[time_slot][person - 1] = 'X'
    current = current.next

table_data = []
for time_slot in time_slots:
    row = [time_slot] + availability_table[time_slot]
    table_data.append(row)

print("\nAvailability:")
print(tabulate(table_data, headers=["Time"] + [f"Person {i+1}" for i in range(5)]))

available_counts = {}
for time_slot in time_slots:
    count = availability_table[time_slot].count('X')
    available_counts[time_slot] = count

max_available_count = max(available_counts.values())
suggested_slots = [time_slot for time_slot, count in available_counts.items() if count == max_available_count]

print("\nSuggested Time Slot(s) with the highest availability:")
for slot in suggested_slots:
    print(f"- {slot} (Majority of {max_available_count} people available)")

# Ask for user preference
preferred_time_frame = input("\nWhat part of the day would you like to be recommended for the Suggested Time Slot (morning/afternoon/evening)? ").lower()

# Function to suggest time slots based on time frame
def suggest_time_slot(time_slots):
    if time_slots:
        suggested_slot = time_slots[0]  # Take the first slot in the filtered list
        print(f"\nSuggested Time Slot: {suggested_slot} (Majority of {max_available_count} people available)")
    else:
        print("No available time slots in this time frame.")

# Filter suggested slots based on user preference
if preferred_time_frame == "morning":
    morning_slots = []
    for slot in suggested_slots:
        if is_morning(int(slot.split(":")[0])):
            morning_slots.append(slot)
    if morning_slots:
        suggest_time_slot(morning_slots)
    else:
        print("No available time slots in the morning.")
elif preferred_time_frame == "afternoon":
    afternoon_slots = []
    for slot in suggested_slots:
        if is_afternoon(int(slot.split(":")[0])):
            afternoon_slots.append(slot)
    if afternoon_slots:
        suggest_time_slot(afternoon_slots)
    else:
        print("No available time slots in the afternoon.")
elif preferred_time_frame == "evening":
    evening_slots = []
    for slot in suggested_slots:
        if is_evening(int(slot.split(":")[0])):
            evening_slots.append(slot)
    if evening_slots:
        suggest_time_slot(evening_slots)
    else:
        print("No available time slots in the evening.")
else:
    print("Invalid preference. Displaying the suggested time slot for the whole day.")
    suggest_time_slot(suggested_slots)


