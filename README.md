# Trip Itinerary PDF Generator

A minimalist tool to create beautiful, clean trip itinerary PDFs with flight info, hotel stays, activities, and more.

## Features

### Web Interface 🌐
- 📝 **Interactive Form** - Easy-to-use web interface for entering trip details
- ➕ **Dynamic Fields** - Add/remove days and events on the fly
- 🎨 **Live Customization** - See your changes reflected immediately
- 📥 **Instant Download** - Generate and download PDFs with one click
- 💡 **Smart Fields** - Context-aware input fields based on event type

### PDF Output 📄
- 🎨 **Minimalist Design** - Clean, modern, easy-to-read layout
- 🎯 **Color-Coded Events** - Different colors for flights, hotels, activities, restaurants, and transport
- 📱 **Organized by Days** - Clear day-by-day structure
- ✈️ **Multiple Event Types** - Supports flights, hotels, activities, restaurants, transport, and custom events
- 📄 **Professional Quality** - PDFs ready to print or share

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### Option 1: Web Interface (Recommended) 🌐

Launch the interactive web UI where you can enter your trip details:

```bash
streamlit run app.py
```

Or use the convenient start script:

```bash
./start_app.sh
```

This will open a web interface in your browser where you can:
- Fill in trip details with a user-friendly form
- Add/remove days and events dynamically
- Generate and download PDFs instantly
- See live preview of your itinerary structure

**Using the Web Interface:**
1. Enter your trip name (required)
2. Add destination and date range (optional)
3. For each day:
   - Enter the date
   - Add events (flight, hotel, activity, etc.)
   - Fill in event-specific details
4. Click "Generate PDF"
5. Download your beautifully formatted itinerary!

### Option 2: Python Script

#### Generate Sample PDF

Run the included sample to see what the output looks like:

```bash
python trip_pdf_generator.py
```

This will generate `sample_trip_itinerary.pdf` with a sample European trip.

#### Create Your Own Trip

1. Copy and modify `example_custom_trip.py`:

```bash
python example_custom_trip.py
```

2. Or create your own script using the trip data structure:

```python
from trip_pdf_generator import generate_pdf_from_data

my_trip = {
    'title': 'My Amazing Trip',
    'destination': 'Destination Name',
    'dates': 'Date Range',
    'days': [
        {
            'day_number': 1,
            'date': 'Monday, January 1',
            'events': [
                {
                    'type': 'flight',
                    'time': '10:00 AM',
                    'airline': 'Airline Name Flight#',
                    'from': 'Origin Airport',
                    'to': 'Destination Airport',
                    'confirmation': 'ABC123'
                },
                # Add more events...
            ]
        },
        # Add more days...
    ]
}

generate_pdf_from_data(my_trip, "my_trip.pdf")
```

## Event Types

The generator supports these event types with color coding:

- **FLIGHT** 🔵 Blue - Airlines, airports, flight numbers
- **HOTEL** 🔴 Red - Hotel check-ins, accommodations
- **ACTIVITY** 🟢 Green - Tours, sightseeing, attractions
- **RESTAURANT** 🟠 Orange - Dining reservations
- **TRANSPORT** 🟣 Purple - Taxis, shuttles, trains
- **OTHER** ⚪ Gray - Any other event

## Event Fields

You can include any fields you want in an event. Common fields:

```python
{
    'type': 'flight',           # Event type (required)
    'time': '10:00 AM',         # Time (optional)
    'airline': '...',           # Custom field
    'from': '...',              # Custom field
    'to': '...',                # Custom field
    'confirmation': '...',      # Custom field
    'notes': '...',             # Custom field
    # Add any other fields you need!
}
```

All fields except `type` and `time` will be displayed in the details section of the event.

## Customization

### Change Colors

Edit the `color_map` in `trip_pdf_generator.py`:

```python
color_map = {
    'FLIGHT': '#3498db',    # Change to your preferred hex color
    'HOTEL': '#e74c3c',
    # ...
}
```

### Modify Styles

The PDF uses custom styles that can be adjusted in the `_setup_custom_styles()` method:

- `TripTitle` - Main title style
- `TripSubtitle` - Destination and date style
- `DayHeader` - Day header style
- `EventType` - Event type label style
- `EventDetails` - Event details text style

## Examples

### Flight Event
```python
{
    'type': 'flight',
    'time': '10:30 AM',
    'airline': 'Air France AF 334',
    'from': 'New York JFK',
    'to': 'Paris CDG',
    'confirmation': 'ABC123XYZ',
    'seat': '14A',
    'terminal': 'Terminal 1'
}
```

### Hotel Event
```python
{
    'type': 'hotel',
    'time': '3:00 PM',
    'name': 'The Grand Hotel',
    'address': '123 Main Street',
    'check_in': 'June 15',
    'check_out': 'June 18',
    'confirmation': 'HTL456789',
    'phone': '+1 555-1234'
}
```

### Activity Event
```python
{
    'type': 'activity',
    'time': '9:00 AM',
    'name': 'City Walking Tour',
    'address': 'Meet at City Hall',
    'duration': '3 hours',
    'guide': 'John - +1 555-9999',
    'notes': 'Bring comfortable shoes and water'
}
```

## License

Free to use and modify as needed.

## Tips

- Keep event details concise for better readability
- Use consistent time formats (e.g., "10:00 AM" or "10:00")
- Include confirmation numbers for easy reference
- Add notes field for important reminders
- Group related events on the same day

Enjoy your trip! ✈️

