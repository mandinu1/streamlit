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
            folium.Marker([7.144840, 80.920700], popup="Victoria Randenigala", tooltip="Liberty Bell").add_to(m)
            folium.Circle(
                radius=100,
                location=[7.544840, 81.920700],
                popup="Liberty Bell",
                color="crimson",
                fill=True,
            ).add_to(m)
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

        provider_counts = (
            filtered_data.groupby("PROVIDER")[board_key].sum().to_dict()
        )

    # Display provider counts dynamically or use placeholder if no data
    if provider_counts:
        for provider, count in provider_counts.items():
            st.write(f"{provider} Board Count: {count}")
    else:
        st.write("No board data available.")


# POSM View
elif page == "POSM":
    st.title("POSM View")