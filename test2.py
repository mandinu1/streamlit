import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_extras.stylable_container import stylable_container
import pandas as pd
if "board_type" not in st.session_state:
    st.session_state.board_type = None


# HOME PAGE
# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio('Select View', ["Board", "POSM", "new1"], key="page_selector")

# Board View
if page == "Board":
    bcol1, bcol2, bcol3 = st.sidebar.columns(3)

    with bcol1:
        with stylable_container(
            key="name_board",
            css_styles="""
                button {
                    background-color: #32a6a8;
                    color: white;
                    width: 100%;
                }
            """
        ):
            if st.button("Name Board", key="name_board"):
                st.session_state.board_type = "Name Board"

    with bcol2:
        with stylable_container(
            key="tin_board",
            css_styles="""
                button {
                    background-color: #1ddbde;
                    color: white;
                    width: 100%;
                }
            """
        ):
            if st.button("Tin Board", key="tin_board"):
                st.session_state.board_type = "Tin Board"

    with bcol3:
        with stylable_container(
            key="side_board",
            css_styles="""
                button {
                    background-color: #02f1f5;
                    color: white;
                    width: 100%;
                }
            """
        ):
            if st.button("Side Board", key="side_board"):
                st.session_state.board_type = "Side Board"
     
    provider = st.sidebar.selectbox(
            "Select Operator",
            ["Dialog", "Mobitel", "Hutch", "Airtel", "All"],
            key="operator_selector",index=4
        )

        # Display the selected operator
    st.write(f"Selected Operator: {provider}")
    if st.session_state.board_type:
        st.write(f"Selected Board: {st.session_state.board_type}")



    st.title("Board View")
    if st.session_state.board_type != "Choose an option":
            # Display Map
            st.header("Retailer Locations Map")
            m = folium.Map(location=[7.873054, 80.771797], zoom_start=7)  # Centered in Sri Lanka
            folium.Marker([7.144840, 80.920700], popup=folium.Popup('<img src="https://upload.wikimedia.org/wikipedia/commons/9/90/VictoriaDam-SriLanka-April2011-1.jpg" width="200px">', max_width=300), tooltip="Liberty Bell").add_to(m)
            st_data = st_folium(m, width=1200, height=800)
    st.header("Provider Board Counts")
    provider_counts = {}
    filtered_data = pd.DataFrame()  # Define filtered_data as an empty DataFrame or load your data here
    if not filtered_data.empty:
        # Assuming filtered_data has columns 'PROVIDER' and board-specific counts
        if st.session_state.board_type == "Name Board":
            board_key = "NAME_BOARD"
        elif st.session_state.board_type == "Tin Board":
            board_key = "TIN_BOARD"
        elif st.session_state.board_type == "Side Board":
            board_key = "SIDE_BOARD"




    # Define provider counts (example counts)
    provider_counts = {
        "Dialog": 50,
        "Mobitel": 30,
        "Hutch": 20,
        "Airtel": 10,
        "Non Dialog": 40,
    }

    # Define colors for each provider
    provider_colors = {
        "Dialog": "#f56642",  # light Red
        "Mobitel": "#008000",  # Green
        "Hutch": "#FFA500",  # Orange
        "Airtel": "#FF0000",  # Red
        "Non Dialog": "#808080",  # Gray
    }

    # Create the UI
    st.title("Provider Counts")

    # Iterate through the providers and display styled buttons with counts
    for provider, count in provider_counts.items():
        col1, col2 = st.columns([1, 1])  # Two-column layout
        with col1:
            # Styled button for the provider
            with stylable_container(
                key=f"{provider}_container",  # Unique key for each provider
                css_styles=f"""
                    button {{
                        background-color: {provider_colors[provider]};
                        font-weight: bold;
                        color: black;
                        width: 100%;
                        height: 50px;
                        border: none;
                        font-size: 18px;
                        text-align: center;
                    }}
                """
            ):
                st.button(provider, key=f"{provider}_button")  # Unique key for each button
        with col2:
            # Count display in bold black
            st.markdown(
                f"""
                <div style="background-color: #F5F5F5; 
                            text-align: center; 
                            font-size: 18px; 
                            font-weight: bold; 
                            color: black; 
                            padding: 10px; 
                            border-radius: 5px;">
                    {count}
                </div>
                """,
                unsafe_allow_html=True,
            )






# POSM View
elif page == "POSM":
    st.title("POSM View")


    # Provider percentages
    provider_percentages = {
        "Dialog": {"value": 60, "color": "red"},
        "Mobitel": {"value": 40, "color": "green"},
        "Hutch": {"value": 20, "color": "orange"},
        "Airtel": {"value": 35, "color": "red"},
    }

    st.title("Provider Percentages")

    # Function to create a horizontal bar for each provider
    def create_percentage_bar(provider, percentage, color):
        return f"""
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="width: 100px; font-weight: bold;">{provider}</div>
            <div style="background-color: #f0f0f0; width: 300px; height: 20px; border-radius: 5px; overflow: hidden; margin-left: 10px;">
                <div style="background-color: {color}; width: {percentage}%; height: 100%; text-align: right; color: white; padding-right: 5px; font-weight: bold;">
                    {percentage}%
                </div>
            </div>
        </div>
        """

    # Generate bars for all providers
    bars_html = ""
    for provider, details in provider_percentages.items():
        bars_html += create_percentage_bar(provider, details["value"], details["color"])

    # Render the bars using markdown
    st.markdown(bars_html, unsafe_allow_html=True)
