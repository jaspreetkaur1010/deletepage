import streamlit as st
import requests
import json

# API Endpoints and API Keys
FETCH_API_URL = "https://f5jimtq9y6.execute-api.eu-north-1.amazonaws.com/default/fetch"
FETCH_API_KEY = "ddN1bWCIv77bjKR36apzw3o8LecsbEBH9i43vNa4"
PUSH_API_URL = "https://6r6i3fdun6.execute-api.eu-north-1.amazonaws.com/default/input"
PUSH_API_KEY = "10F2075pRv77qROyukUV464voCCItZRUrNdf4Xa7"

# Headers for API requests
FETCH_HEADERS = {
    "x-api-key": FETCH_API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

PUSH_HEADERS = {
    "x-api-key": PUSH_API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Functions for fetching and updating modules and cakes
def fetch_modules(auth_code):
    try:
        response = requests.post(FETCH_API_URL, headers=FETCH_HEADERS, json={"auth_code": auth_code})
        response_data = response.json()
        if response.status_code == 200:
            return response_data.get("modules", [])
        else:
            st.error("Failed to fetch modules. Please check the API or your auth code.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching modules: {e}")
        return []

def push_modules(auth_code, modules):
    try:
        payload = {"auth_code": auth_code, "modules": modules}
        response = requests.post(PUSH_API_URL, headers=PUSH_HEADERS, json=payload)
        if response.status_code == 200:
            st.success("✅ Modules and cakes updated successfully!")
        else:
            st.error("❌ Failed to push modules. Check the API or data format.")
            st.write("Response:", response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error pushing modules: {e}")

# Function to delete a module
def delete_module():
    module_names = [module["module_name"] for module in st.session_state.modules]
    selected_module = st.selectbox("📦 Select the Module to Delete", module_names, key="delete_module_select")

    if selected_module:
        if st.text_input("🔑 Enter Password to Confirm Module Deletion", type="password", key="delete_module_password") == "SIVI":
            st.write(f"### ⚠️ Module Selected for Deletion: {selected_module}")
            if st.button("🗑️ Confirm Delete Module"):
                module_index = module_names.index(selected_module)
                st.session_state.modules.pop(module_index)
                st.success(f"✅ Module '{selected_module}' deleted successfully!")
        else:
            st.error("❌ Incorrect password. Deletion aborted.")

# Function to delete a cake from a module
def delete_cake():
    module_names = [module["module_name"] for module in st.session_state.modules]
    selected_module = st.selectbox("🍰 Select the Module from which to Delete a Cake", module_names, key="delete_cake_module_select")
    
    if selected_module:
        module_index = module_names.index(selected_module)
        cake_names = [cake.get("displayname", "Unnamed Cake") for cake in st.session_state.modules[module_index].get("cakes_content_json", [])]
        
        if cake_names:
            selected_cake = st.selectbox("🎂 Select the Cake to Delete", cake_names, key="delete_cake_select")

            if st.button("🗑️ Delete Selected Cake"):
                cake_index = cake_names.index(selected_cake)
                st.session_state.modules[module_index]["cakes_content_json"].pop(cake_index)
                st.success(f"✅ Cake '{selected_cake}' deleted successfully!")
        else:
            st.warning("⚠️ No cakes available in the selected module to delete.")

# Main function
def main():
    st.set_page_config(page_title="DELETE CAKES AND MODULES", layout="centered")
    st.title("🗑️ Delete Cakes and Modules Manager")

    # Input auth_code for this session
    auth_code = st.text_input("🔑 Enter Auth Code", type="password")

    if st.button("🔍 Fetch Modules"):
        if auth_code:
            modules = fetch_modules(auth_code)
            if modules:
                st.session_state.modules = modules
        else:
            st.error("❌ Please enter a valid auth code.")

    if "modules" not in st.session_state:
        st.session_state.modules = []

    if st.session_state.modules:
        st.write("### 🗂️ Delete Modules or Cakes")
        action = st.selectbox("🛠️ What do you want to delete?", ["Select...", "Module", "Cake"], key="delete_action")

        if action == "Module":
            delete_module()

        elif action == "Cake":
            delete_cake()

        # Push updates after deletion
        if st.button("📤 Push Updates", key="push_updates"):
            push_modules(auth_code, st.session_state.modules)

if __name__ == "__main__":
    main()
