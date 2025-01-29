import streamlit as st
import mysql.connector
import bcrypt
import urllib.parse

# Database connection function
def connect_to_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="12345", database="travell"
    )

# Function to validate user login
def validate_user(username, password):
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and bcrypt.checkpw(password.encode('utf-8'), result['password'].encode('utf-8')):
        return result
    else:
        return None

# Function to create a new user (Sign Up)
def create_user(username, password):
    # Hash the password before saving it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

# Function to logout user
def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    # Clear all session state variables if needed
    st.session_state.clear()
    st.write("You have been logged out.")

# Streamlit App
st.title("ExploreNext: Travel Insights Portal")

# Add background image using HTML and CSS
st.markdown("""
    <style>
    body {
        background-image: url('https://www.bing.com/ck/a?!&&p=2c665a3f54b97de698d80474402cc816e21a520927a9d05e9ff5081593c3d7e1JmltdHM9MTczODAyMjQwMA&ptn=3&ver=2&hsh=4&fclid=04a7fdaa-dda2-6c9e-2488-ed47dc396d5a&u=a1L2ltYWdlcy9zZWFyY2g_cT10cmF2ZWwlMjB3YWxscGFwZXImRk9STT1JUUZSQkEmaWQ9MzMwQkE4M0RCMkRERDUyN0IwMUMxNTRBREFFQUM4QTQyQ0FBQjNCRA&ntb=1');
        background-size: cover;
        background-position: center;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state for login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Login or Sign Up Section
if not st.session_state["logged_in"]:
    st.subheader("Login or Sign Up to ExploreNext")
    
    # Option to switch between Login and Sign Up
    option = st.radio("Choose an option", ["Login", "Sign Up"])

    if option == "Login":
        # Login form
        username = st.text_input("Enter your Username")
        password = st.text_input("Enter your Password", type="password")
        
        if st.button("Login"):
            # Validate user credentials
            user = validate_user(username, password)
            
            if user:
                st.success(f"Welcome {username}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("Invalid username or password. Please try again.")

    elif option == "Sign Up":
        # Sign Up form
        new_username = st.text_input("Enter your Username (new)")
        new_password = st.text_input("Enter your Password (new)", type="password")
        confirm_password = st.text_input("Confirm your Password", type="password")

        if st.button("Sign Up"):
            if new_password == confirm_password:
                # Check if username already exists
                conn = connect_to_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Users WHERE username = %s", (new_username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    st.error("Username already taken. Please choose another.")
                else:
                    # Create the new user
                    create_user(new_username, new_password)
                    st.success("Account created successfully! You can now log in.")
                cursor.close()
                conn.close()
            else:
                st.error("Passwords do not match. Please try again.")

# Main Dashboard (only if logged in)
if st.session_state["logged_in"]:
    st.subheader(f"Welcome {st.session_state['username']}!")

    # Logout Button
    if st.button("Logout"):
        logout()
        st.session_state["logged_in"] = False  # Manually set this to False to simulate logout
        st.stop()  # Stops further execution and reloads the app

    # Allow user to input Upcoming or Completed Travels only if logged in
    st.header("Enter Your Travel Information")
    travel_type = st.radio("Select Travel Type", ["Upcoming Travel", "Completed Travel"])

    if travel_type == "Upcoming Travel":
        st.subheader("Enter Upcoming Travel Details")
        destination = st.text_input("Destination (Type destination here)")
        travel_date = st.date_input("Travel Date")
        duration = st.number_input("Duration (in days)", min_value=1)

        if st.button("Submit Upcoming Travel"):
            # Insert the upcoming travel data into the database
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO UpcomingTravels (user_name, destination, travel_date, duration) VALUES (%s, %s, %s, %s)",
                           (st.session_state["username"], destination, travel_date, duration))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Upcoming Travel information saved successfully!")

    elif travel_type == "Completed Travel":
        st.subheader("Enter Completed Travel Details")
        destination = st.text_input("Destination")
        feedback = st.text_area("Feedback")
        travel_date = st.date_input("Travel Date")
        duration = st.number_input("Duration (in days)", min_value=1)
        image_path = st.text_input("Image Path (Optional)")

        if st.button("Submit Completed Travel"):
            # Insert the completed travel data into the database
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CompletedTravels (user_name, destination, feedback, travel_date, duration, image_path) VALUES (%s, %s, %s, %s, %s, %s)",
                           (st.session_state["username"], destination, feedback, travel_date, duration, image_path))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Completed Travel information saved successfully!")

    # Display Upcoming Travels (User-specific data)
    st.header("Your Upcoming Travels")
    if st.button("Show Your Upcoming Travels"):
        try:
            conn = connect_to_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM UpcomingTravels WHERE user_name = %s", (st.session_state['username'],))
            results = cursor.fetchall()

            if results:
                for row in results:
                    st.write(f"Destination: {row['destination']}, Travel Date: {row['travel_date']}, Duration: {row['duration']} days")
            else:
                st.write("No upcoming travels found.")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # **Public Display of Completed Travels** - Visible to all users
    st.header("Completed Travels - Take Feedback from Others")
    keyword = st.text_input("Search Feedback by Keyword")
    search_button = st.button("Search Feedback")

    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        
        if search_button:
            if keyword:
                # Query to fetch feedback matching the keyword
                query = "SELECT * FROM CompletedTravels WHERE feedback LIKE %s OR destination LIKE %s"
                cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
                results = cursor.fetchall()
                
                if results:
                    for row in results:
                        st.write(f"Destination: {row['destination']}, Feedback: {row['feedback']}, Travel Date: {row['travel_date']}, Duration: {row['duration']} days")
                        if row['image_path']:
                            st.image(row['image_path'], caption=f"Image of {row['destination']}", use_column_width=True)
                else:
                    st.write("No matching feedback found.")
            else:
                st.error("Please enter a keyword to search.")
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
