# ============================================
# CROP RECOMMENDATION SYSTEM
# app.py — Main Flask Application
# ============================================

# --- Imports ---
from flask import Flask, render_template, request
import joblib        # for loading our saved ML model
import numpy as np   # for converting inputs to array
import os            # for building file paths

# --- Create Flask app ---
app = Flask(__name__)

# ============================================
# LOAD THE TRAINED MODEL
# We load it ONCE when the app starts
# so we don't reload it on every request
# ============================================

# Build the path to our saved model
# os.path.join works correctly on all OS
MODEL_PATH = os.path.join('models', 'crop_model.pkl')

# Load the model into memory
model = joblib.load(MODEL_PATH)

print(f"Model loaded successfully!")
print(f"Model can predict: {len(model.classes_)} crops")

# ============================================
# CROP INFO DICTIONARY
# Provides extra info about each predicted crop
# ============================================
CROP_INFO = {
    'rice'        : {'emoji': '🌾', 'season': 'Kharif',  'water': 'High'},
    'maize'       : {'emoji': '🌽', 'season': 'Kharif',  'water': 'Medium'},
    'chickpea'    : {'emoji': '🫘', 'season': 'Rabi',    'water': 'Low'},
    'kidneybeans' : {'emoji': '🫘', 'season': 'Kharif',  'water': 'Medium'},
    'pigeonpeas'  : {'emoji': '🫘', 'season': 'Kharif',  'water': 'Low'},
    'mothbeans'   : {'emoji': '🫘', 'season': 'Kharif',  'water': 'Low'},
    'mungbean'    : {'emoji': '🫘', 'season': 'Kharif',  'water': 'Low'},
    'blackgram'   : {'emoji': '🫘', 'season': 'Kharif',  'water': 'Low'},
    'lentil'      : {'emoji': '🫘', 'season': 'Rabi',    'water': 'Low'},
    'pomegranate' : {'emoji': '🍎', 'season': 'Annual',  'water': 'Low'},
    'banana'      : {'emoji': '🍌', 'season': 'Annual',  'water': 'High'},
    'mango'       : {'emoji': '🥭', 'season': 'Summer',  'water': 'Medium'},
    'grapes'      : {'emoji': '🍇', 'season': 'Annual',  'water': 'Medium'},
    'watermelon'  : {'emoji': '🍉', 'season': 'Summer',  'water': 'High'},
    'muskmelon'   : {'emoji': '🍈', 'season': 'Summer',  'water': 'Medium'},
    'apple'       : {'emoji': '🍎', 'season': 'Annual',  'water': 'Medium'},
    'orange'      : {'emoji': '🍊', 'season': 'Annual',  'water': 'Medium'},
    'papaya'      : {'emoji': '🍈', 'season': 'Annual',  'water': 'High'},
    'coconut'     : {'emoji': '🥥', 'season': 'Annual',  'water': 'Medium'},
    'cotton'      : {'emoji': '🌿', 'season': 'Kharif',  'water': 'Medium'},
    'jute'        : {'emoji': '🌿', 'season': 'Kharif',  'water': 'High'},
    'coffee'      : {'emoji': '☕', 'season': 'Annual',  'water': 'Medium'},
}

# ============================================
# ROUTE 1: Homepage
# ============================================
@app.route('/')
def home():
    """Render the homepage with the input form."""
    return render_template('index.html')


# ============================================
# ROUTE 2: Prediction
# methods=['POST'] means this route only
# accepts form submissions, not direct visits
# ============================================
@app.route('/predict', methods=['POST'])
def predict():
    """
    Receive form data, run prediction,
    and return the result page.
    """
    try:
        # ----------------------------------------
        # STEP 1: Read inputs from the form
        # request.form contains all submitted values
        # float() converts text to decimal number
        # ----------------------------------------
        nitrogen    = float(request.form['nitrogen'])
        phosphorus  = float(request.form['phosphorus'])
        potassium   = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity    = float(request.form['humidity'])
        ph          = float(request.form['ph'])
        rainfall    = float(request.form['rainfall'])

        # ----------------------------------------
        # STEP 2: Validate input ranges
        # Protect against unrealistic values
        # ----------------------------------------
        errors = []

        if not (0 <= nitrogen <= 140):
            errors.append("Nitrogen must be between 0 and 140")
        if not (0 <= phosphorus <= 145):
            errors.append("Phosphorus must be between 0 and 145")
        if not (0 <= potassium <= 205):
            errors.append("Potassium must be between 0 and 205")
        if not (0 <= temperature <= 50):
            errors.append("Temperature must be between 0 and 50")
        if not (0 <= humidity <= 100):
            errors.append("Humidity must be between 0 and 100")
        if not (0 <= ph <= 14):
            errors.append("pH must be between 0 and 14")
        if not (0 <= rainfall <= 300):
            errors.append("Rainfall must be between 0 and 300")

        # If any validation failed, return error page
        if errors:
            return render_template(
                'result.html',
                error=True,
                error_messages=errors
            )

        # ----------------------------------------
        # STEP 3: Package inputs into numpy array
        # The model expects a 2D array:
        # [[N, P, K, temp, humidity, ph, rainfall]]
        # reshape(1, -1) converts to correct shape
        # ----------------------------------------
        input_data = np.array([[
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall
        ]])

        # ----------------------------------------
        # STEP 4: Make prediction
        # model.predict() returns crop name
        # model.predict_proba() returns confidence
        # ----------------------------------------
        prediction  = model.predict(input_data)[0]
        proba       = model.predict_proba(input_data)[0]
        confidence  = round(max(proba) * 100, 2)

        # ----------------------------------------
        # STEP 5: Get extra crop information
        # Use .get() with default in case crop
        # is not in our CROP_INFO dictionary
        # ----------------------------------------
        crop_details = CROP_INFO.get(prediction, {
            'emoji'  : '🌱',
            'season' : 'Varies',
            'water'  : 'Medium'
        })

        # ----------------------------------------
        # STEP 6: Package all inputs to display
        # back to user on result page
        # ----------------------------------------
        user_inputs = {
            'Nitrogen'    : nitrogen,
            'Phosphorus'  : phosphorus,
            'Potassium'   : potassium,
            'Temperature' : f"{temperature} C",
            'Humidity'    : f"{humidity} %",
            'pH'          : ph,
            'Rainfall'    : f"{rainfall} mm"
        }

        # ----------------------------------------
        # STEP 7: Render result page with all data
        # We pass variables to the HTML template
        # ----------------------------------------
        return render_template(
            'result.html',
            error       = False,
            crop        = prediction,
            confidence  = confidence,
            crop_details= crop_details,
            user_inputs = user_inputs
        )

    # ----------------------------------------
    # CATCH any unexpected errors
    # Shows a friendly error instead of crashing
    # ----------------------------------------
    except ValueError:
        return render_template(
            'result.html',
            error         = True,
            error_messages= ["Please enter valid numbers in all fields."]
        )
    except Exception as e:
        return render_template(
            'result.html',
            error         = True,
            error_messages= [f"An unexpected error occurred: {str(e)}"]
        )


# ============================================
# RUN THE APP
# ============================================
if __name__ == '__main__':
    app.run(debug=True)