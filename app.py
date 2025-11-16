"""
Trip Itinerary PDF Generator - Web UI
Interactive web interface to create trip itinerary PDFs
"""

import streamlit as st
from trip_pdf_generator import generate_pdf_from_data
import os
from datetime import datetime

st.set_page_config(
    page_title="Trip Itinerary PDF Generator",
    page_icon="✈️",
    layout="wide"
)

# Initialize session state
if 'days' not in st.session_state:
    st.session_state.days = [{'events': [{}]}]

# Initialize custom event types
if 'custom_event_types' not in st.session_state:
    st.session_state.custom_event_types = {
        'flight': '#3498db',
        'hotel': '#e74c3c',
        'activity': '#2ecc71',
        'restaurant': '#f39c12',
        'transport': '#9b59b6',
        'other': '#95a5a6'
    }

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #1f77b4;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">✈️ Trip Itinerary PDF Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Create beautiful, minimalist trip itinerary PDFs</div>', unsafe_allow_html=True)

# Trip Info Section
st.header("📋 Trip Information")
col1, col2, col3 = st.columns(3)

with col1:
    trip_title = st.text_input("Trip Name *", placeholder="e.g., European Adventure")
with col2:
    destination = st.text_input("Destination", placeholder="e.g., Paris → Rome → Barcelona")
with col3:
    dates = st.text_input("Dates", placeholder="e.g., June 15-25, 2024")

st.markdown("---")

# Event Types Section
st.header("🎨 Event Types")

with st.expander("Customize Event Types (Optional)", expanded=False):
    st.markdown("Add custom event types or modify the default ones:")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        new_type_name = st.text_input("Event Type Name", key="new_type_name", placeholder="e.g., Car Rental")
    with col2:
        new_type_color = st.color_picker("Color", key="new_type_color", value="#3498db")
    with col3:
        st.write("")  # Spacer
        st.write("")  # Spacer
        if st.button("➕ Add Type"):
            if new_type_name:
                type_key = new_type_name.lower().replace(' ', '_')
                st.session_state.custom_event_types[type_key] = new_type_color
                st.success(f"Added '{new_type_name}'!")
                st.rerun()
    
    # Display current event types
    st.markdown("**Current Event Types:**")
    types_to_remove = []
    
    for event_type, color in st.session_state.custom_event_types.items():
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"**{event_type.replace('_', ' ').title()}**")
        with col2:
            # Color preview
            st.markdown(f'<div style="background-color: {color}; padding: 8px; border-radius: 4px; color: white; text-align: center;">{color}</div>', unsafe_allow_html=True)
        with col3:
            if st.button("🗑️", key=f"remove_type_{event_type}"):
                types_to_remove.append(event_type)
    
    # Remove types after iteration
    for type_to_remove in types_to_remove:
        del st.session_state.custom_event_types[type_to_remove]
        st.rerun()

st.markdown("---")

# Days Section
st.header("📅 Daily Itinerary")

# Function to add a new day
def add_day():
    st.session_state.days.append({'events': [{}]})

# Function to remove a day
def remove_day(day_idx):
    if len(st.session_state.days) > 1:
        st.session_state.days.pop(day_idx)

# Function to add event to a day
def add_event(day_idx):
    st.session_state.days[day_idx]['events'].append({})

# Function to remove event from a day
def remove_event(day_idx, event_idx):
    if len(st.session_state.days[day_idx]['events']) > 1:
        st.session_state.days[day_idx]['events'].pop(event_idx)

# Display each day
for day_idx, day in enumerate(st.session_state.days):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Day {day_idx + 1}")
    with col2:
        if len(st.session_state.days) > 1:
            if st.button(f"🗑️ Remove Day", key=f"remove_day_{day_idx}"):
                remove_day(day_idx)
                st.rerun()
    
    # Day details
    col1, col2 = st.columns(2)
    with col1:
        day_date = st.text_input(
            "Date",
            key=f"day_date_{day_idx}",
            placeholder="e.g., Saturday, June 15"
        )
    
    st.markdown("**Events:**")
    
    # Display each event in this day
    for event_idx, event in enumerate(day['events']):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**Event {event_idx + 1}**")
        with col2:
            if len(day['events']) > 1:
                if st.button("❌", key=f"remove_event_{day_idx}_{event_idx}"):
                    remove_event(day_idx, event_idx)
                    st.rerun()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            # Get list of available event types
            available_types = list(st.session_state.custom_event_types.keys())
            event_type = st.selectbox(
                "Event Type *",
                available_types,
                key=f"event_type_{day_idx}_{event_idx}",
                format_func=lambda x: x.replace('_', ' ').title()
            )
        with col2:
            event_time = st.text_input(
                "Time",
                key=f"event_time_{day_idx}_{event_idx}",
                placeholder="e.g., 10:30 AM"
            )
        
        # Store basic info
        st.session_state.days[day_idx]['events'][event_idx]['type'] = event_type
        st.session_state.days[day_idx]['events'][event_idx]['time'] = event_time
        
        # Event-specific fields based on type
        if event_type == "flight":
            col1, col2, col3 = st.columns(3)
            with col1:
                airline = st.text_input("Airline/Flight #", key=f"airline_{day_idx}_{event_idx}")
                if airline:
                    st.session_state.days[day_idx]['events'][event_idx]['airline'] = airline
            with col2:
                from_loc = st.text_input("From", key=f"from_{day_idx}_{event_idx}")
                if from_loc:
                    st.session_state.days[day_idx]['events'][event_idx]['from'] = from_loc
            with col3:
                to_loc = st.text_input("To", key=f"to_{day_idx}_{event_idx}")
                if to_loc:
                    st.session_state.days[day_idx]['events'][event_idx]['to'] = to_loc
            
            col1, col2 = st.columns(2)
            with col1:
                confirmation = st.text_input("Confirmation #", key=f"confirmation_{day_idx}_{event_idx}")
                if confirmation:
                    st.session_state.days[day_idx]['events'][event_idx]['confirmation'] = confirmation
            with col2:
                seat = st.text_input("Seat", key=f"seat_{day_idx}_{event_idx}")
                if seat:
                    st.session_state.days[day_idx]['events'][event_idx]['seat'] = seat
        
        elif event_type == "hotel":
            col1, col2 = st.columns(2)
            with col1:
                hotel_name = st.text_input("Hotel Name", key=f"hotel_name_{day_idx}_{event_idx}")
                if hotel_name:
                    st.session_state.days[day_idx]['events'][event_idx]['name'] = hotel_name
            with col2:
                address = st.text_input("Address", key=f"address_{day_idx}_{event_idx}")
                if address:
                    st.session_state.days[day_idx]['events'][event_idx]['address'] = address
            
            col1, col2, col3 = st.columns(3)
            with col1:
                check_in = st.text_input("Check-in", key=f"checkin_{day_idx}_{event_idx}")
                if check_in:
                    st.session_state.days[day_idx]['events'][event_idx]['check_in'] = check_in
            with col2:
                check_out = st.text_input("Check-out", key=f"checkout_{day_idx}_{event_idx}")
                if check_out:
                    st.session_state.days[day_idx]['events'][event_idx]['check_out'] = check_out
            with col3:
                confirmation = st.text_input("Confirmation #", key=f"conf_{day_idx}_{event_idx}")
                if confirmation:
                    st.session_state.days[day_idx]['events'][event_idx]['confirmation'] = confirmation
        
        elif event_type == "activity":
            col1, col2 = st.columns(2)
            with col1:
                activity_name = st.text_input("Activity Name", key=f"activity_name_{day_idx}_{event_idx}")
                if activity_name:
                    st.session_state.days[day_idx]['events'][event_idx]['name'] = activity_name
            with col2:
                address = st.text_input("Location/Address", key=f"location_{day_idx}_{event_idx}")
                if address:
                    st.session_state.days[day_idx]['events'][event_idx]['address'] = address
            
            col1, col2 = st.columns(2)
            with col1:
                duration = st.text_input("Duration", key=f"duration_{day_idx}_{event_idx}")
                if duration:
                    st.session_state.days[day_idx]['events'][event_idx]['duration'] = duration
            with col2:
                ticket = st.text_input("Ticket/Confirmation", key=f"ticket_{day_idx}_{event_idx}")
                if ticket:
                    st.session_state.days[day_idx]['events'][event_idx]['confirmation'] = ticket
        
        elif event_type == "restaurant":
            col1, col2 = st.columns(2)
            with col1:
                restaurant_name = st.text_input("Restaurant Name", key=f"restaurant_name_{day_idx}_{event_idx}")
                if restaurant_name:
                    st.session_state.days[day_idx]['events'][event_idx]['name'] = restaurant_name
            with col2:
                address = st.text_input("Address", key=f"rest_address_{day_idx}_{event_idx}")
                if address:
                    st.session_state.days[day_idx]['events'][event_idx]['address'] = address
            
            col1, col2 = st.columns(2)
            with col1:
                reservation = st.text_input("Reservation", key=f"reservation_{day_idx}_{event_idx}")
                if reservation:
                    st.session_state.days[day_idx]['events'][event_idx]['reservation'] = reservation
            with col2:
                phone = st.text_input("Phone", key=f"phone_{day_idx}_{event_idx}")
                if phone:
                    st.session_state.days[day_idx]['events'][event_idx]['phone'] = phone
        
        elif event_type == "transport":
            col1, col2 = st.columns(2)
            with col1:
                transport_details = st.text_input("Details", key=f"transport_details_{day_idx}_{event_idx}")
                if transport_details:
                    st.session_state.days[day_idx]['events'][event_idx]['details'] = transport_details
            with col2:
                company = st.text_input("Company/Service", key=f"company_{day_idx}_{event_idx}")
                if company:
                    st.session_state.days[day_idx]['events'][event_idx]['company'] = company
        
        else:  # Custom event types or "other"
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name/Title", key=f"other_name_{day_idx}_{event_idx}")
                if name:
                    st.session_state.days[day_idx]['events'][event_idx]['name'] = name
            with col2:
                location = st.text_input("Location", key=f"custom_location_{day_idx}_{event_idx}")
                if location:
                    st.session_state.days[day_idx]['events'][event_idx]['location'] = location
            
            col1, col2 = st.columns(2)
            with col1:
                details = st.text_input("Details", key=f"other_details_{day_idx}_{event_idx}")
                if details:
                    st.session_state.days[day_idx]['events'][event_idx]['details'] = details
            with col2:
                confirmation = st.text_input("Confirmation/Reference", key=f"custom_conf_{day_idx}_{event_idx}")
                if confirmation:
                    st.session_state.days[day_idx]['events'][event_idx]['confirmation'] = confirmation
        
        # Notes field for all event types
        notes = st.text_area(
            "Notes",
            key=f"notes_{day_idx}_{event_idx}",
            placeholder="Any additional notes or reminders..."
        )
        if notes:
            st.session_state.days[day_idx]['events'][event_idx]['notes'] = notes
    
    # Add event button
    if st.button(f"➕ Add Event to Day {day_idx + 1}", key=f"add_event_{day_idx}"):
        add_event(day_idx)
        st.rerun()
    
    # Store day date
    if day_date:
        st.session_state.days[day_idx]['date'] = day_date

# Add day button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("➕ Add Another Day", use_container_width=True):
        add_day()
        st.rerun()

st.markdown("---")

# Generate PDF Section
st.header("🎨 Generate PDF")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    output_filename = st.text_input(
        "PDF Filename",
        value="my_trip_itinerary.pdf",
        help="Name for your PDF file"
    )
    
    if st.button("🚀 Generate PDF", type="primary", use_container_width=True):
        if not trip_title:
            st.error("❌ Please enter a trip name!")
        else:
            try:
                # Build trip data structure
                trip_data = {
                    'title': trip_title,
                    'destination': destination if destination else None,
                    'dates': dates if dates else None,
                    'days': []
                }
                
                # Process each day
                for day_idx, day in enumerate(st.session_state.days):
                    day_data = {
                        'day_number': day_idx + 1,
                        'date': day.get('date', ''),
                        'events': []
                    }
                    
                    # Process each event
                    for event in day['events']:
                        # Only add events that have a type
                        if 'type' in event and event['type']:
                            # Remove empty string values
                            clean_event = {k: v for k, v in event.items() if v}
                            if clean_event:  # Only add if not empty
                                day_data['events'].append(clean_event)
                    
                    # Only add day if it has events
                    if day_data['events']:
                        trip_data['days'].append(day_data)
                
                # Generate PDF with custom colors
                generate_pdf_from_data(trip_data, output_filename, st.session_state.custom_event_types)
                
                st.success(f"✅ PDF generated successfully: {output_filename}")
                
                # Provide download button
                if os.path.exists(output_filename):
                    with open(output_filename, "rb") as file:
                        st.download_button(
                            label="📥 Download PDF",
                            data=file,
                            file_name=output_filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")

# Sidebar with tips
with st.sidebar:
    st.header("💡 Tips")
    
    # Show current event type colors
    st.markdown("**Your Event Types:**")
    for event_type, color in st.session_state.custom_event_types.items():
        color_icon = f'<span style="display:inline-block; width:12px; height:12px; background-color:{color}; border-radius:2px; margin-right:5px;"></span>'
        st.markdown(f'{color_icon}**{event_type.replace("_", " ").title()}**', unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("""
    **Pro Tips:**
    - Customize event types in the "Event Types" section
    - Add confirmation numbers for easy reference
    - Use consistent time formats (e.g., "10:00 AM")
    - Include addresses for easy navigation
    - Add notes for important reminders
    - Keep events in chronological order
    
    **Quick Start:**
    1. Enter trip name (required)
    2. (Optional) Customize event types
    3. Add destination and dates (optional)
    4. Fill in events for each day
    5. Click "Generate PDF"
    6. Download your itinerary!
    """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

