"""
Example: Create your own custom trip itinerary
"""

from trip_pdf_generator import generate_pdf_from_data

# Define your trip data
my_trip = {
    'title': 'Weekend Getaway',
    'destination': 'San Francisco',
    'dates': 'March 20-23, 2024',
    'days': [
        {
            'day_number': 1,
            'date': 'Friday, March 20',
            'events': [
                {
                    'type': 'flight',
                    'time': '8:00 AM',
                    'airline': 'United UA 1234',
                    'from': 'Los Angeles LAX',
                    'to': 'San Francisco SFO',
                    'confirmation': 'ABCD123'
                },
                {
                    'type': 'hotel',
                    'time': '11:00 AM',
                    'name': 'The St. Regis San Francisco',
                    'address': '125 3rd St, San Francisco, CA 94103',
                    'check_in': 'March 20',
                    'check_out': 'March 23',
                    'confirmation': 'HTL987654'
                },
                {
                    'type': 'restaurant',
                    'time': '7:00 PM',
                    'name': 'Gary Danko',
                    'address': '800 North Point St',
                    'reservation': 'Confirmed for 2'
                }
            ]
        },
        {
            'day_number': 2,
            'date': 'Saturday, March 21',
            'events': [
                {
                    'type': 'activity',
                    'time': '10:00 AM',
                    'name': 'Golden Gate Bridge Walk',
                    'notes': 'Start at welcome center, walk to first tower'
                },
                {
                    'type': 'activity',
                    'time': '2:00 PM',
                    'name': 'Alcatraz Tour',
                    'confirmation': 'ALC456789',
                    'notes': 'Ferry departs from Pier 33'
                }
            ]
        },
        {
            'day_number': 3,
            'date': 'Sunday, March 22',
            'events': [
                {
                    'type': 'activity',
                    'time': '9:00 AM',
                    'name': 'Farmers Market',
                    'address': 'Ferry Building Marketplace',
                    'notes': 'Open until 2 PM'
                },
                {
                    'type': 'other',
                    'time': '3:00 PM',
                    'name': 'Free Time',
                    'notes': 'Explore Haight-Ashbury or Chinatown'
                }
            ]
        }
    ]
}

# Generate the PDF
generate_pdf_from_data(my_trip, "my_custom_trip.pdf")

