# BMI Calculator (Advanced) — Oasis Infobyte Internship

**Internship:** Oasis Infobyte — Python Programming Internship
**Task:** Task 2 — BMI Calculator (Advanced / GUI + Database + Visualization version)
**Author:** Tarun Sonaji

## Project Description

A desktop **BMI (Body Mass Index) Calculator** built with **Python and Tkinter**.
The application calculates a user's BMI, classifies it into a standard health
category with color-coded feedback, stores every calculation in a local
**SQLite** database, and lets the user review their history and view a
**BMI trend graph** over time using **Matplotlib**.

The app supports multiple users — each user's records are stored and can be
viewed or plotted separately.

## Features

- Clean, dedicated Tkinter GUI with a header, input form, and action buttons.
- Calculates BMI using the standard formula and rounds it to 2 decimal places.
- Classifies BMI into **Underweight / Normal / Overweight / Obese**.
- Color-coded result display (amber / green / orange / red) based on category.
- Robust input validation:
  - Empty fields
  - Non-numeric weight/height
  - Zero or negative values
  - Unrealistic values (e.g. height > 3 m, weight > 500 kg)
  - Invalid user names (must start with a letter; only letters, spaces,
    hyphens and apostrophes allowed)
  - All errors are shown as clear Tkinter message boxes — the app never
    crashes on bad input.
- Multi-user support: each record is tagged with the user's name.
- Automatic SQLite database creation on first run (`bmi_data.db`), with a
  table created automatically if it doesn't already exist.
- **Save Record** button to store the current calculation.
- **View History** window: a sortable table of past records, filterable by
  user (or "All Users").
- **Show BMI Trend** window: a Matplotlib line chart of a selected user's
  BMI over time, with reference lines at the 18.5 / 25 / 30 category
  boundaries. Handles the case where a user has no records yet.
- **Clear** button to reset the form, and **Exit** to close the app.
- Uses a relative database path, so the project works the same way after
  being cloned onto any Windows computer.

## Technologies Used

- Python 3.11+
- Tkinter (standard library) — GUI
- sqlite3 (standard library) — data storage
- Matplotlib — BMI trend visualization

## BMI Formula

```
BMI = weight (kg) / (height (m) * height (m))
```

## BMI Categories

| BMI Range        | Category     |
|-------------------|-------------|
| BMI < 18.5         | Underweight |
| 18.5 – 24.9        | Normal      |
| 25 – 29.9          | Overweight  |
| BMI >= 30          | Obese       |

## Installation Instructions

1. Make sure **Python 3.11 or newer** is installed on Windows and available
   on your `PATH`. Tkinter and `sqlite3` ship with the standard Python
   installer, so no extra steps are needed for them.
2. Clone or download this repository, then navigate to the project folder:

   ```
   git clone https://github.com/TarunSonaji/OIBSIP
   cd OIBSIP/Python-Task2-BMICalculator
   ```

3. (Recommended) Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install the required dependency:

   ```
   pip install -r requirements.txt
   ```

## How to Run the Application

From inside the `Python-Task2-BMICalculator` folder, run:

```
python bmi_calculator.py
```

The application window will open, and a `bmi_data.db` SQLite file will be
created automatically in the same folder the first time you run it.

## Project Structure

```
Python-Task2-BMICalculator/
│
├── bmi_calculator.py     # Main application (GUI + logic + database)
├── requirements.txt      # External dependency (matplotlib)
├── README.md             # Project documentation
├── bmi_data.db           # Created automatically on first run (not tracked)
└── screenshots/          # App screenshots (added after running the app)
```

## Example Usage

1. Launch the app with `python bmi_calculator.py`.
2. Enter a name (e.g. `Tarun`), weight in kg (e.g. `70`), and height in
   meters (e.g. `1.75`).
3. Click **Calculate BMI** — the app displays the BMI value and category
   with a matching color.
4. Click **Save Record** to store the result in the database.
5. Click **View History** to see all saved records, optionally filtered by
   user.
6. Click **Show BMI Trend** to see a line chart of a selected user's BMI
   over time.
7. Click **Clear** to reset the form for a new entry, or **Exit** to close
   the app.

## Error Handling

- Empty name, weight, or height fields are rejected with a clear message.
- Non-numeric weight/height values are caught and reported without
  crashing the app.
- Zero, negative, or unrealistic weight/height values are rejected.
- Invalid user names (numbers, symbols, or names starting with a non-letter)
  are rejected.
- Database errors (e.g. file/permission issues) are caught and shown in a
  message box instead of crashing the application.
- The BMI Trend window gracefully shows an informational message when there
  is no data yet for the selected (or any) user, instead of failing.

## Future Improvements

- Add the ability to edit or delete individual saved records.
- Add unit conversion (pounds/inches) alongside kilograms/meters.
- Export history to CSV or PDF.
- Add user authentication/login for stricter multi-user separation.
- Add BMI targets and personalized recommendations.

## Author

**Tarun Sonaji**
Oasis Infobyte — Python Programming Internship
GitHub: https://github.com/TarunSonaji/OIBSIP

## 🎥 Demo Video

Check out the working demo of the BMI Calculator:

🔗 **[Watch the Demo Video on LinkedIn](https://www.linkedin.com/posts/tarun-sonaji-8161b6332_oasisinfobyte-python-pythonprogramming-ugcPost-7506334999554469888-SQ8X/?utm_source=social_share_send&utm_medium=android_app&rcm=ACoAAFOt1BIBnLaTO5l8x_KvLks41x1yXCzpgXk&utm_campaign=copy_link)**

The demo demonstrates:

* BMI calculation
* BMI category/result display
* Input validation
* BMI history
* BMI trend visualization
