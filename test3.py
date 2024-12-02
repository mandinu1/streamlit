import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
from io import BytesIO
import base64

# Filepaths for the CSVs
filepath_name_board = r'C:/Users/Chamoda_10657/Desktop/brand_app/NAME_BOARD_SUMMARY_GEO_STORE_N.csv'
filepath_tin_board = r'C:/Users/Chamoda_10657/Desktop/brand_app/TIN_BOARD_SUMMARY_GEO_STORE_N.csv'
filepath_side_board = r'C:/Users/Chamoda_10657/Desktop/brand_app/SIDE_BOARD_SUMMARY_GEO_STORE_N.csv'
filepath_posm = r'C:/Users/Chamoda_10657/Desktop/brand_app/BRAND_PRESENSE_SUMMARY_GEO_STORE_N.csv'

# Cache the data loading function
@st.cache_data
def load_data(filepath):
    return pd.read_csv(filepath)

# Load all datasets
data_name_board = load_data(filepath_name_board)
data_tin_board = load_data(filepath_tin_board)
data_side_board = load_data(filepath_side_board)
data_posm = load_data(filepath_posm)

# Function to update the cache based on board type
def update_board_type_data(board_type):
    if board_type == "Name Board":
        return data_name_board
    elif board_type == "Tin Board":
        return data_tin_board
    elif board_type == "Side Board":
        return data_side_board
    else:
        return pd.DataFrame()

# Navigation Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select View", ["Board", "POSM"])

# Board View
if page == "Board":
    st.title("Board View")

    # Board type selection
    board_type = st.selectbox(
        "Select Board Type",
        options=["Choose an option", "Name Board", "Tin Board", "Side Board"]
    )

    # Update session state and clear cache when board type changes
    if "board_type" in st.session_state and st.session_state.board_type != board_type:
        if "filtered_data" in st.session_state:
            del st.session_state.filtered_data
        st.session_state.board_type = board_type
    elif "board_type" not in st.session_state:
        st.session_state.board_type = board_type

    if board_type != "Choose an option":
        st.sidebar.header("Filters")

        # Province selection
        province_options = ["Choose an option"] + sorted(data_name_board["PROVINCE"].dropna().unique().astype(str).tolist())
        province = st.sidebar.selectbox("Select Province", options=province_options)
        
        # District selection
        if province != "Choose an option":
            filtered_data = data_name_board[data_name_board["PROVINCE"].astype(str) == province]
            district_options = ["Choose an option"] + sorted(filtered_data["DISTRICT"].dropna().unique().astype(str).tolist())
        else:
            district_options = ["Choose an option"]

        district = st.sidebar.selectbox("Select District", options=district_options)

        # DS Division selection
        if district != "Choose an option":
            filtered_data = filtered_data[filtered_data["DISTRICT"].astype(str) == district]
            ds_division_options = ["Choose an option"] + sorted(filtered_data["DS_DIVISION"].dropna().unique().astype(str).tolist())
        else:
            ds_division_options = ["Choose an option"]

        ds_division = st.sidebar.selectbox("Select DS Division", options=ds_division_options)

        # Store Name selection
        if ds_division != "Choose an option":
            filtered_data = filtered_data[filtered_data["DS_DIVISION"].astype(str) == ds_division]
            store_name_options = ["Choose an option"] + sorted(filtered_data["PROFILE_NAME"].dropna().unique().astype(str).tolist())
        else:
            store_name_options = ["Choose an option"]

        store_name = st.sidebar.selectbox("Select Retailer Name (in DSR)", options=store_name_options)

        # Apply Filters button
        apply_filters = st.sidebar.button("Apply Filters")
        if apply_filters or "filtered_data" not in st.session_state:
            filtered_data = update_board_type_data(board_type)

            if province != "Choose an option":
                filtered_data = filtered_data[filtered_data["PROVINCE"].astype(str) == province]
            if district != "Choose an option":
                filtered_data = filtered_data[filtered_data["DISTRICT"].astype(str) == district]
            if ds_division != "Choose an option":
                filtered_data = filtered_data[filtered_data["DS_DIVISION"].astype(str) == ds_division]
            if store_name != "Choose an option":
                filtered_data = filtered_data[filtered_data["PROFILE_NAME"].astype(str) == store_name]

            st.session_state.filtered_data = filtered_data

        if "filtered_data" in st.session_state:
            filtered_data = st.session_state.filtered_data

            # Render Retailer Locations
            st.header("Retailer Locations")
            if not filtered_data.empty:
                # Sri Lanka's approximate bounds
                southwest = [6.0, 82.5]
                northeast = [9.8, 82.0]
                m = folium.Map(location=[7.8731, 80.7718], zoom_start=7)
                m.fit_bounds([southwest, northeast])
                for _, row in filtered_data.iterrows():
                    if pd.notna(row["LATITUDE"]) and pd.notna(row["LONGITUDE"]):
                        folium.Marker(
                            location=[row["LATITUDE"], row["LONGITUDE"]],
                            popup=row["PROFILE_NAME"],
                            tooltip=row["PROFILE_NAME"]
                        ).add_to(m)

                st_folium(m, width=1200, height=800)
            else:
                st.warning("No locations available for the selected filters.")

            # Render Provider Board Counts
            st.header("Provider Board Counts")
            provider_counts = {}
            if not filtered_data.empty:
                if board_type == "Name Board":
                    board_key = "NAME_BOARD"
                elif board_type == "Tin Board":
                    board_key = "TIN_BOARD"
                elif board_type == "Side Board":
                    board_key = "SIDE_BOARD"

                provider_counts["Dialog"] = filtered_data[f"DIALOG_{board_key}"].sum()
                provider_counts["Mobitel"] = filtered_data[f"MOBITEL_{board_key}"].sum()
                provider_counts["Airtel"] = filtered_data[f"AIRTEL_{board_key}"].sum()
                provider_counts["Hutch"] = filtered_data[f"HUTCH_{board_key}"].sum()

                for provider, count in provider_counts.items():
                    st.write(f"{provider} Board Count: {count}")
            else:
                st.warning("No provider board data available for the selected filters.")

            # Render Retailer Shop Image
            st.header("Retailer Shop Image")
            if apply_filters and store_name != "Choose an option":
                retailer_data = filtered_data[filtered_data["PROFILE_NAME"] == store_name]
                if not retailer_data.empty:
                    base64_image = retailer_data.iloc[0]["IMAGE"]
                    try:
                        image_data = base64.b64decode(base64_image)
                        img = Image.open(BytesIO(image_data))
                        st.image(img, caption=f"Retailer: {store_name}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Could not load image for {store_name}: {e}")
                else:
                    st.warning("No image found for the selected retailer.")
            else:
                st.warning("Please select a retailer to view the image.")







elif page == "POSM":
    # Page for 'POSM' selection
    st.title("POSM View")

    # Cascading filters (All filters always visible)
    st.sidebar.header("Filters")

    # Check if 'PROVINCE' column exists before trying to access it
    if 'PROVINCE' in data_posm.columns:
        # Province selection
        province = st.sidebar.selectbox(
            "Select Province", 
            options=["Choose an option"] + sorted(data_posm["PROVINCE"].dropna().unique().tolist())
        )
    else:
        province = "Choose an option"
        st.error("The 'PROVINCE' column is not available in the selected data.")

    # Filter districts based on province
    if province != "Choose an option":
        filtered_data = data_posm[data_posm["PROVINCE"] == province]
    else:
        filtered_data = data_posm  # Default dataset for "Choose an option"

    district = st.sidebar.selectbox(
        "Select District", 
        options=["Choose an option"] + sorted(filtered_data["DISTRICT"].dropna().unique().tolist())
    )

    # Filter DS Division based on district
    if district != "Choose an option":
        filtered_data = filtered_data[filtered_data["DISTRICT"] == district]
    ds_division = st.sidebar.selectbox(
        "Select DS Division", 
        options=["Choose an option"] + sorted(filtered_data["DS_DIVISION"].dropna().unique().tolist())
    )

    # Filter data based on DS Division
    if ds_division != "Choose an option":
        filtered_data = filtered_data[filtered_data["DS_DIVISION"] == ds_division]

    store_name = st.sidebar.selectbox(
        "Select Retailer Name (in DSR)", 
        options=["Choose an option"] + sorted(filtered_data["PROFILE_NAME"].dropna().unique().tolist())
    )

    # Filter data based on retailer name
    if store_name != "Choose an option":
        filtered_data = filtered_data[filtered_data["PROFILE_NAME"] == store_name]

    # Create an Apply Filter button to trigger data update
    apply_filters = st.sidebar.button("Apply Filters")

    # Ensure the results are not cleared on each rerun
    if "filtered_posm_data" not in st.session_state:
        st.session_state.filtered_posm_data = data_posm  # Default to the whole dataset

    if "province" not in st.session_state:
        st.session_state.province = province
    
    if "district" not in st.session_state:
        st.session_state.district = district
    
    if "ds_division" not in st.session_state:
        st.session_state.ds_division = ds_division
    
    if "store_name" not in st.session_state:
        st.session_state.store_name = store_name

    # Apply filter only when the button is clicked
    if apply_filters:
        # Store filtered data into session state
        st.session_state.filtered_posm_data = filtered_data

    # Use the filtered data stored in session state
    filtered_data = st.session_state.filtered_posm_data

    if "filtered_posm_data" in st.session_state:
        filtered_data = st.session_state.filtered_posm_data
        # Filtered data should reflect all applied filters
        filtered_data = filtered_data.dropna(subset=["LATITUDE", "LONGITUDE"])  # Ensure valid location data

        # Render Retailer Locations
        st.header("Retailer Locations")
        if not filtered_data.empty:
            # Sri Lanka's approximate bounds
            southwest = [6.0, 82.5]
            northeast = [9.8, 82.0]
            m = folium.Map(location=[7.8731, 80.7718], zoom_start=7)
            m.fit_bounds([southwest, northeast])

            for _, row in filtered_data.iterrows():
                if pd.notna(row["LATITUDE"]) and pd.notna(row["LONGITUDE"]):
                    folium.Marker(
                        location=[row["LATITUDE"], row["LONGITUDE"]],
                        popup=row["PROFILE_NAME"],
                        tooltip=row["PROFILE_NAME"]
                    ).add_to(m)

            st_folium(m, width=1200, height=800)
        else:
            st.warning("No locations available for the selected filters.")

    st.header("Provider POSM Percentages")

    if not st.session_state.filtered_posm_data.empty:
        # Replace NaN values with 0 for percentage columns
        st.session_state.filtered_posm_data = st.session_state.filtered_posm_data.fillna({
            "DIALOG_AREA_PERCENTAGE": 0,
            "MOBITEL_AREA_PERCENTAGE": 0,
            "AIRTEL_AREA_PERCENTAGE": 0,
            "HUTCH_AREA_PERCENTAGE": 0
        })

        # Calculate the sum of percentages for each store (should be 100 for each store)
        total_percentages = st.session_state.filtered_posm_data[[ 
            "DIALOG_AREA_PERCENTAGE", 
            "MOBITEL_AREA_PERCENTAGE", 
            "AIRTEL_AREA_PERCENTAGE", 
            "HUTCH_AREA_PERCENTAGE"
        ]].sum(axis=1)

        # Calculate weighted averages to keep the sum close to 100%
        weighted_avg_dialog = (st.session_state.filtered_posm_data["DIALOG_AREA_PERCENTAGE"] / total_percentages).mean() * 100
        weighted_avg_mobitel = (st.session_state.filtered_posm_data["MOBITEL_AREA_PERCENTAGE"] / total_percentages).mean() * 100
        weighted_avg_airtel = (st.session_state.filtered_posm_data["AIRTEL_AREA_PERCENTAGE"] / total_percentages).mean() * 100
        weighted_avg_hutch = (st.session_state.filtered_posm_data["HUTCH_AREA_PERCENTAGE"] / total_percentages).mean() * 100

        # Display weighted averages
        st.write(f"Dialog Percentage: {weighted_avg_dialog:.2f}%")
        st.write(f"Mobitel Percentage: {weighted_avg_mobitel:.2f}%")
        st.write(f"Airtel Percentage: {weighted_avg_airtel:.2f}%")
        st.write(f"Hutch Percentage: {weighted_avg_hutch:.2f}%")
    else:
        st.write("No data available for the selected filters.")

    # Display POSM Images for Retailer
    st.header("Retailer Image")
    if store_name != "Choose an option" and store_name != "":
        retailer_data = filtered_data[filtered_data["PROFILE_NAME"] == store_name]
        if not retailer_data.empty:
            base64_image = retailer_data.iloc[0]["IMAGE"]  # Get base64 string
            try:
                image_data = base64.b64decode(base64_image)
                img = Image.open(BytesIO(image_data))
                st.image(img, caption=f"Retailer: {store_name}", use_container_width=True)
            except Exception as e:
                st.error(f"Could not load image for {store_name}: {e}")
    else:
        # Display caption without image
        st.write("No Retailer Selected")

else:
    # Default state: no filters applied, show message
    st.write("Select filters and click 'Apply Filters' to see data.")
