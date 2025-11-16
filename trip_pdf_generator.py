"""
Trip Itinerary PDF Generator
A minimalist tool to create beautiful trip itinerary PDFs
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from datetime import datetime


class TripPDFGenerator:
    """Generate minimalist trip itinerary PDFs"""
    
    def __init__(self, output_filename="trip_itinerary.pdf"):
        self.output_filename = output_filename
        self.doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []
    
    def _setup_custom_styles(self):
        """Create custom minimalist styles"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='TripTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='TripSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#666666'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Day header style
        self.styles.add(ParagraphStyle(
            name='DayHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceBefore=24,
            spaceAfter=12,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=0,
            borderColor=colors.HexColor('#e0e0e0'),
            borderRadius=None,
            backColor=None
        ))
        
        # Event type style
        self.styles.add(ParagraphStyle(
            name='EventType',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#ffffff'),
            fontName='Helvetica-Bold',
            leftIndent=0,
            rightIndent=0
        ))
        
        # Event details style
        self.styles.add(ParagraphStyle(
            name='EventDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica',
            leading=14
        ))
        
        # Event label style
        self.styles.add(ParagraphStyle(
            name='EventLabel',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#888888'),
            fontName='Helvetica',
            leading=12
        ))
    
    def add_title(self, trip_name, destination=None, dates=None):
        """Add trip title and basic info"""
        self.story.append(Spacer(1, 0.3*inch))
        
        # Trip name
        title = Paragraph(trip_name, self.styles['TripTitle'])
        self.story.append(title)
        
        # Subtitle with destination and dates
        subtitle_parts = []
        if destination:
            subtitle_parts.append(destination)
        if dates:
            subtitle_parts.append(dates)
        
        if subtitle_parts:
            subtitle = Paragraph(" • ".join(subtitle_parts), self.styles['TripSubtitle'])
            self.story.append(subtitle)
        else:
            self.story.append(Spacer(1, 0.3*inch))
    
    def add_day(self, day_number, date, events):
        """Add a day section with events"""
        
        # Day header
        day_header = f"Day {day_number}"
        if date:
            day_header += f" • {date}"
        
        header = Paragraph(day_header, self.styles['DayHeader'])
        self.story.append(header)
        
        # Add each event
        for event in events:
            self._add_event(event)
        
        self.story.append(Spacer(1, 0.15*inch))
    
    def _add_event(self, event):
        """Add a single event (flight, hotel, activity, etc.)"""
        
        event_type = event.get('type', 'Event').upper()
        time = event.get('time', '')
        
        # Color coding for different event types
        color_map = {
            'FLIGHT': '#3498db',
            'HOTEL': '#e74c3c',
            'ACTIVITY': '#2ecc71',
            'RESTAURANT': '#f39c12',
            'TRANSPORT': '#9b59b6',
            'OTHER': '#95a5a6'
        }
        
        bg_color = colors.HexColor(color_map.get(event_type, color_map['OTHER']))
        
        # Create event table
        data = []
        
        # Header row with event type and time
        header_text = f"<para align=left><b>{event_type}</b></para>"
        time_text = f"<para align=right>{time}</para>" if time else ""
        
        header_row = [
            Paragraph(header_text, self.styles['EventType']),
            Paragraph(time_text, self.styles['EventType'])
        ]
        data.append(header_row)
        
        # Create the table
        table = Table(data, colWidths=[5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), bg_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        self.story.append(table)
        
        # Event details
        details_data = []
        
        # Add all detail fields
        for key, value in event.items():
            if key not in ['type', 'time'] and value:
                label = key.replace('_', ' ').title()
                
                # Format the detail row
                label_para = Paragraph(f"<b>{label}:</b>", self.styles['EventLabel'])
                value_para = Paragraph(str(value), self.styles['EventDetails'])
                
                details_data.append([label_para, value_para])
        
        if details_data:
            details_table = Table(details_data, colWidths=[1.2*inch, 5.3*inch])
            details_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
            ]))
            
            self.story.append(details_table)
        
        self.story.append(Spacer(1, 0.2*inch))
    
    def generate(self):
        """Generate the PDF file"""
        self.doc.build(self.story)
        print(f"✅ PDF generated successfully: {self.output_filename}")


def create_sample_trip():
    """Create a sample trip itinerary"""
    
    trip_data = {
        'title': 'European Adventure',
        'destination': 'Paris → Rome → Barcelona',
        'dates': 'June 15-25, 2024',
        'days': [
            {
                'day_number': 1,
                'date': 'Saturday, June 15',
                'events': [
                    {
                        'type': 'flight',
                        'time': '10:30 AM',
                        'airline': 'Air France AF 334',
                        'from': 'New York JFK',
                        'to': 'Paris CDG',
                        'confirmation': 'ABC123XYZ'
                    },
                    {
                        'type': 'transport',
                        'time': '3:00 PM',
                        'details': 'Airport shuttle to hotel',
                        'company': 'Paris Shuttle Service'
                    },
                    {
                        'type': 'hotel',
                        'time': '4:30 PM',
                        'name': 'Hotel Le Marais',
                        'address': '12 Rue des Archives, 75004 Paris',
                        'check_in': 'June 15',
                        'check_out': 'June 18',
                        'confirmation': 'HTL456789'
                    }
                ]
            },
            {
                'day_number': 2,
                'date': 'Sunday, June 16',
                'events': [
                    {
                        'type': 'activity',
                        'time': '9:00 AM',
                        'name': 'Eiffel Tower Visit',
                        'address': 'Champ de Mars, 5 Avenue Anatole',
                        'notes': 'Skip-the-line tickets already purchased'
                    },
                    {
                        'type': 'restaurant',
                        'time': '1:00 PM',
                        'name': 'Le Petit Cler',
                        'address': '29 Rue Cler, 75007 Paris',
                        'reservation': 'Confirmed for 2 people',
                        'notes': 'Try the duck confit!'
                    },
                    {
                        'type': 'activity',
                        'time': '3:30 PM',
                        'name': 'Louvre Museum',
                        'address': 'Rue de Rivoli, 75001 Paris',
                        'notes': 'Timed entry at 3:30 PM - Ticket #ML789456'
                    }
                ]
            },
            {
                'day_number': 3,
                'date': 'Monday, June 17',
                'events': [
                    {
                        'type': 'activity',
                        'time': '10:00 AM',
                        'name': 'Montmartre Walking Tour',
                        'meeting_point': 'Place du Tertre',
                        'guide': 'Marie - +33 6 12 34 56 78'
                    },
                    {
                        'type': 'restaurant',
                        'time': '7:00 PM',
                        'name': 'L\'Ami Jean',
                        'address': '27 Rue Malar, 75007 Paris',
                        'reservation': 'Confirmed - mention Booking.com'
                    }
                ]
            }
        ]
    }
    
    return trip_data


def generate_pdf_from_data(trip_data, output_filename="trip_itinerary.pdf"):
    """
    Generate a PDF from trip data dictionary
    
    Args:
        trip_data: Dictionary containing trip information
        output_filename: Name of output PDF file
    """
    
    generator = TripPDFGenerator(output_filename)
    
    # Add title
    generator.add_title(
        trip_data.get('title', 'Trip Itinerary'),
        trip_data.get('destination'),
        trip_data.get('dates')
    )
    
    # Add each day
    for day in trip_data.get('days', []):
        generator.add_day(
            day.get('day_number'),
            day.get('date'),
            day.get('events', [])
        )
    
    # Generate the PDF
    generator.generate()


if __name__ == "__main__":
    # Generate sample trip PDF
    sample_trip = create_sample_trip()
    generate_pdf_from_data(sample_trip, "sample_trip_itinerary.pdf")

