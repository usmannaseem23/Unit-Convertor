import streamlit as st
import pint

# Initialize the unit registry
ureg = pint.UnitRegistry()
ureg.default_format = "~P"

# Function to convert units
def convert_units(value, from_unit, to_unit):  
    try:
        # Handle temperature conversion separately due to offset issue
        if from_unit in ["celsius", "fahrenheit", "kelvin"] and to_unit in ["celsius", "fahrenheit", "kelvin"]:
            temp = ureg.Quantity(value, ureg.parse_expression(from_unit))
            result = temp.to(ureg.parse_expression(to_unit)).magnitude  # Extract magnitude
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        else:
            # Handle other unit conversions normally
            result = (value * ureg(from_unit)).to(to_unit)
            return f"{value} {from_unit} = {result:.2f} {to_unit}"

    except pint.errors.DimensionalityError:
        return "❌ Invalid conversion"
    except ValueError:
        return "❌ Please enter a valid numeric value."
    except Exception as e:
        return f"❌ Error: {e}"

# Page Configuration
st.set_page_config(page_title="Unit Converter", page_icon="🔢", layout="wide")

# Sidebar Theme Settings
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("🎨 Select Theme:", ["🌞 Light Mode", "🌙 Dark Mode"])

# Theme Colors
theme_colors = {
    "🌞 Light Mode": {"bg": "#FFFFFF", "text": "#000000", "input": "#F5F5F5", "btn": "#007BFF", "sidebar": "#F0F0F0"},
    "🌙 Dark Mode": {"bg": "#222831", "text": "#FFFFFF", "input": "#2d2f36", "btn": "#00ADB5", "sidebar": "#000000"},
}
colors = theme_colors[theme]

# Apply CSS Styling
st.markdown(f"""
    <style>
        .stApp {{ background-color: {colors['bg']}; color: {colors['text']} !important; }}
        section[data-testid="stSidebar"] {{ background-color: {colors['sidebar']} !important; color: {colors['text']} !important; }}
        input, textarea, select {{ background-color: {colors['input']} !important; color: {colors['text']} !important; }}
        .stButton>button {{ background-color: {colors['btn']}; color: white; border-radius: 8px; padding: 10px 16px; transition: 0.3s; }}
        .stButton>button:hover {{ background-color: darken({colors['btn']}, 10%); }}
        label, .stMarkdown, .stRadio, .stSelectbox, .stTextInput, .stTextArea, .stExpander, h1, h2, h3, h4, h5, h6, p, span {{ color: {colors['text']} !important; }}
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
mode = st.sidebar.radio("🔍 Select Options:", ["Unit Converter", "Units & Conversions Table"])

# Main Title
st.title("Unit Converter 🔢")
st.write("Easily convert units with accuracy! 🎯")

# Unit Categories
unit_options = {
    "📏 Length": ["meters", "feet", "kilometers", "miles", "centimeters", "inches"],
    "⚖️ Weight": ["kilograms", "pounds", "grams", "ounces"],
    "🌡️ Temperature": ["celsius", "fahrenheit", "kelvin"],
    "🧪 Volume": ["liters", "gallons", "milliliters", "cups"]
}

# Unit Converter
if mode == "Unit Converter":
    st.subheader("Unit Converter")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        value = st.text_input("🔢 Enter Value:", placeholder="e.g., 10")

    with col2:
        category = st.selectbox("📂 Select Unit Type:", list(unit_options.keys()))

    with col3:
        from_unit = st.selectbox("🔄 From Unit:", unit_options[category])
        to_unit = st.selectbox("➡️ To Unit:", unit_options[category])

    if st.button(" Convert Now"):
        try:
            value = float(value)
            result = convert_units(value, from_unit, to_unit)
            st.success(f"✅ {result}")
        except ValueError:
            st.error("❌ Please enter a valid numeric value.")

# Units & Conversions Table
elif mode == "Units & Conversions Table":
    st.subheader("📏 Common Units & Conversions")
    conversion_data = {
        "📏 Length": ["1 meter = 3.281 feet", "1 kilometer = 0.621 miles"],
        "⚖️ Weight": ["1 kilogram = 2.205 pounds", "1 gram = 0.035 ounces"],
        "🌡️ Temperature": ["0°C = 32°F", "100°C = 212°F"],
        "🧪 Volume": ["1 liter = 4.227 cups", "1 gallon = 3.785 liters"],
    }

    for category, conversions in conversion_data.items():
        with st.expander(f" {category}"):
            for conversion in conversions:
                st.write(f"🔹 {conversion}")

# Footer
st.markdown("---")
st.markdown(f"""
<center>
 Developed by <b style='color: {colors['btn']};'>Usman Naseem</b> 🚀 | Powered by <b>Streamlit</b> 
<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="50">
</center>
""", unsafe_allow_html=True)
