from datetime import datetime, timedelta

# Function to calculate the next period date based on the average cycle length
def predict_next_period(last_period_date, cycle_length):
    if isinstance(last_period_date, str):
        try:
            last_period_date = datetime.strptime(last_period_date, '%Y-%m-%d').date()
        except ValueError:
            return "Error: Last period date must be in 'YYYY-MM-DD' format."

    if not isinstance(cycle_length, int) or cycle_length <= 0:
        return "Error: cycle_length must be a positive integer."

    # Predict next period date
    next_period_date = last_period_date + timedelta(days=cycle_length)

    return next_period_date  # Return as a datetime.date object


# Function to calculate the fertile window
def calculate_fertile_window(last_period_date, cycle_length):
    ovulation_day = last_period_date + timedelta(days=(cycle_length // 2))
    fertile_start = ovulation_day - timedelta(days=5)
    fertile_end = ovulation_day + timedelta(days=1)
    return fertile_start, fertile_end


# Function to get user input and validate it
def get_date_input(prompt):
    while True:
        date_input = input(prompt)
        try:
            # Use datetime.strptime directly from the datetime module
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
            return date
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")


# Sample user database (in-memory)
users = {}

# Function to register a new user
def register_user():
    username = input("Create a username: ").strip()
    if username in users:
        print("Username already exists. Try a different one.")
        return None
    name = input("Enter your name: ").strip()
    age = input("Enter your age: ").strip()
    email = input("Enter your email: ").strip()
    cycle_length = int(input("Enter your average cycle length (in days): "))
    last_period_date = get_date_input("Enter the date of your last period (YYYY-MM-DD): ")

    # Collect data for initial history
    history = []
    for i in range(3):  # Assuming we need data for 3 cycles
        date = get_date_input(f"Enter the start date of cycle {i+1} (YYYY-MM-DD): ")
        mood = input(f"Enter mood for cycle {i+1}: ").strip()
        symptoms = input(f"Enter symptoms for cycle {i+1}: ").strip()
        history.append({
            'date': date,
            'mood': mood,
            'symptoms': symptoms
        })

    users[username] = {
        'name': name,
        'age': age,
        'email': email,
        'cycle_length': cycle_length,
        'last_period_date': last_period_date,
        'history': history
    }
    print(f"User {username} registered successfully!\n")
    return username


# Function to check cycle regularity
def check_cycle_regularity(history):
    if len(history) < 3:
        return "Not enough data to determine cycle regularity."
    
    # Calculate the cycle differences between consecutive cycles
    differences = [(history[i] - history[i - 1]).days for i in range(1, len(history))]

    # Calculate the average difference and the standard deviation to assess regularity
    average_difference = sum(differences) / len(differences)
    standard_deviation = (sum([(x - average_difference) ** 2 for x in differences]) / len(differences)) ** 0.5

    # Define a threshold for standard deviation to determine irregularity
    threshold = 2  # This can be adjusted based on the tolerance for variability

    if standard_deviation > threshold:
        return "Your cycle shows significant variability. It's recommended to monitor it closely or consult with a healthcare professional."
    else:
        return "Your cycle appears regular, with minor variability."


# Function to log mood and symptoms
def log_mood_symptoms(username):
    date = get_date_input("Enter the date (YYYY-MM-DD): ")
    mood = input("How are you feeling today? ").strip()
    symptoms = input("Any symptoms to note? ").strip()
    
    users[username]['history'].append({
        'date': date,
        'mood': mood,
        'symptoms': symptoms
    })
    print("Mood and symptoms logged successfully!")


# Function to display cycle information
def display_cycle_info(username):
    user_data = users[username]
    last_period_date = user_data['last_period_date']
    cycle_length = user_data['cycle_length']
    next_period_date = predict_next_period(last_period_date, cycle_length)
    fertile_start, fertile_end = calculate_fertile_window(last_period_date, cycle_length)

    print("\nMenstrual Cycle Information for", user_data['name'])
    print(f"Last Period Date       : {last_period_date.strftime('%Y-%m-%d')}")
    print(f"Average Cycle Length   : {cycle_length} days")
    print(f"Next Period Date       : {next_period_date}")
    print(f"Fertile Window         : {fertile_start.strftime('%Y-%m-%d')} to {fertile_end.strftime('%Y-%m-%d')}")
    print(f"Cycle Regularity       : {check_cycle_regularity([entry['date'] for entry in user_data['history']])}")
    print("\nCycle History and Logs:")
    for entry in user_data['history']:
        print(f"Date: {entry['date']}, Mood: {entry['mood']}, Symptoms: {entry['symptoms']}")


# Function to display cycle visual representation
def display_visual_representation(username):
    user_data = users[username]
    history_dates = sorted([entry['date'] for entry in user_data['history']])
    
    if len(history_dates) < 3:
        print("Not enough cycle history to display visualization.")
        return

    print("\nVisual Representation of Last 3 Cycles:")

    # Print headers
    print("Cycle 1          Cycle 2          Cycle 3          Predicted")

    # Determine cycle dates for the last 3 cycles
    cycle_dates = history_dates[-3:]
    predicted_date = predict_next_period(cycle_dates[-1], user_data['cycle_length'])

    for i in range(3):
        if i < len(cycle_dates):
            start_date = cycle_dates[i]
            end_date = start_date + timedelta(days=user_data['cycle_length'])
            print(f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}", end="   ")
        else:
            print(" " * 17, end="   ")
    
    # Print predicted cycle
    print(f"{predicted_date.strftime('%Y-%m-%d')}")


# Function to provide health tips
def provide_health_tips(username):
    user_data = users[username]
    last_period_date = user_data['last_period_date']
    days_since_last_period = (datetime.now().date() - last_period_date).days

    if days_since_last_period < 7:
        print("\nHealth Tip: It's your Menstrual Phase!! Nurture yourself like a queen 👑! Pamper with relaxation and hydrate your way to comfort 💧")
    elif days_since_last_period < 14:
        print("\nHealth Tip: It's your Follicular Phase!! You’re in full bloom! 🌸 Feel the energy rise, try new workouts 🏋️‍♀️, and nourish with vibrant greens 🥗.")
    elif days_since_last_period < 21:
        print("\nHealth Tip: It's your Ovulation Phase!! You’re radiating! ✨ Embrace your peak energy, stay active 🚴‍♀️, and shine through your day!")
    else:
        print("\nHealth Tip: It's the Luteal Phase. Slow down, but stay fabulous! ✨ Enjoy some deep breaths, herbal teas ☕, and keep your calm vibes strong.")


def main():
    print(" 🎉 Welcome to HerCycle!")
    print("------------------------------------------------------------")
    username = None

    while not username:
        print("Ready to take control of your health? 🗓️  Register now and stay informed every step of the way!\n  ")
        choice = input("Enter 1 to register ✍️ ").strip()
        if choice == '1':
            print("Welcome aboard! 🌷 Let’s make your cycle tracking as natural and beautiful as you are.")
            username = register_user()

    while True:
        print("\nWhat would you like to do?")
        print("1. View Cycle Information")
        print("2. Log Mood and Symptoms")
        print("3. View Cycle Phase Visualization")
        print("4. Get Health Tips")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            display_cycle_info(username)
        elif choice == '2':
            log_mood_symptoms(username)
        elif choice == '3':
            display_visual_representation(username)
        elif choice == '4':
            provide_health_tips(username)
        elif choice == '5':
            print("Thank you for using HerCycle. Stay healthy! Stay Strong 💪 !! and Slay 😉!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
