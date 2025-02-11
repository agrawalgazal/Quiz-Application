from django.core.exceptions import ValidationError
VALID_CITIES=[
    # Global Cities
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego",
    "Dallas", "San Jose", "Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa", "Mexico City", "Guadalajara",
    "Monterrey", "Tijuana", "Leon", "Quebec City", "Edmonton", "Winnipeg", "Boston", "Seattle", "Denver",
    "Las Vegas", "San Francisco", "Miami", "Orlando", "Washington D.C.", "Atlanta", "Charlotte", "Detroit",
    "São Paulo", "Rio de Janeiro", "Buenos Aires", "Lima", "Bogotá", "Santiago", "Caracas", "Medellín", "Quito",
    "London", "Paris", "Berlin", "Madrid", "Rome", "Amsterdam", "Lisbon", "Vienna", "Athens", "Brussels",
    "Lagos", "Cairo", "Johannesburg", "Cape Town", "Nairobi", "Casablanca", "Accra", "Addis Ababa",
    "Tokyo", "Seoul", "Beijing", "Shanghai", "Hong Kong", "Bangkok", "Jakarta", "Manila", "Singapore", "Taipei",
    "Kuala Lumpur", "Hanoi", "Ho Chi Minh City", "Dubai", "Abu Dhabi", "Riyadh", "Jeddah", "Doha", "Tehran",
    # All Cities in India
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur",
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna",
    "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli",
    "Vasai-Virar", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad",
    "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur",
    "Kota", "Guwahati", "Chandigarh", "Solapur", "Hubballi-Dharwad", "Bareilly", "Moradabad", "Mysore", "Gurgaon",
    "Aligarh", "Jalandhar", "Tiruchirappalli", "Bhubaneswar", "Salem", "Mira-Bhayandar", "Thiruvananthapuram",
    "Bhiwandi", "Saharanpur", "Gorakhpur", "Guntur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai",
    "Cuttack", "Firozabad", "Kochi", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Nanded", "Kolhapur",
    "Ajmer", "Akola", "Ujjain", "Tirunelveli", "Belgaum", "Jhansi", "Udaipur", "Siliguri", "Jammu", "Sangli",
    "Bokaro Steel City", "Nellore", "Mangalore", "Tiruppur", "Gaya", "Tirupati", "Shimoga", "Tumkur", "Hosur",
    "Kurnool", "Gandhinagar", "Gandhidham", "Erode", "Pondicherry", "Kollam", "Sagar", "Bardhaman", "Kharagpur",
    "Karimnagar", "Rajahmundry", "Bhusawal", "Hindupur", "Ratlam", "Hazaribagh", "Dhule", "Ambur", "Nizamabad",
    "Chittoor", "Bettiah", "Gangtok", "Shillong", "Aizawl", "Imphal", "Itanagar", "Kohima", "Dimapur",
    "Agartala", "Port Blair", "Panaji", "Margoa", "Puducherry", "Daman", "Silvassa", "Gangtok", "Aizawl",
    "Churu", "Fatehpur", "Dausa", "Gorakhpur", "Jalgaon", "Bilaspur", "Sagar", "Rewa", "Satna", "Bhilwara",
    "Raichur", "Hospet", "Kakinada", "Anantapur", "Bellary", "Hapur", "Shahjahanpur", "Rampur", "Mirzapur",
    "Munger", "Katihar", "Begusarai", "Purnia", "Bhagalpur", "Muzaffarpur", "Gopalganj", "Darbhanga",
    "Arrah", "Bettiah", "Motihari", "Chapra", "Saharsa", "Madhepura", "Supaul", "Sitamarhi", "Samastipur",
    "Siwan", "Vaishali", "Hajipur", "Nalanda", "Buxar", "Jehanabad", "Gaya", "Aurangabad", "Navsari",
    "Porbandar", "Bhuj", "Junagadh", "Jamnagar", "Surendranagar", "Bhavnagar", "Gandhidham", "Mehsana",
    "Anand", "Valsad", "Vapi", "Dahod", "Godhra", "Palanpur", "Morbi", "Modasa", "Amreli", "Gondal", "Botad",
    "Gariadhar", "Una", "Veraval", "Chhatarpur", "Datia", "Tikamgarh", "Sehore", "Vidisha", "Dhar", "Shivpuri",
    "Ashoknagar", "Raisen", "Dewas", "Hoshangabad", "Betul", "Itarsi", "Seoni", "Mandla", "Chhindwara",
    "Balaghat", "Jhabua", "Barwani", "Ratlam", "Mandsaur", "Neemuch", "Bharuch", "Karwar", "Hassan", "Mandya",
    "Chikmagalur", "Davanagere", "Gadag", "Bagalkot", "Haveri", "Dharwad", "Raichur", "Koppal", "Bijapur",
    "Chamarajanagar", "Udupi", "Karwar", "Madikeri", "Bidar", "Gulbarga", "Yadgir", "Shimoga", "Tumkur",
    "Chitradurga", "Chikkaballapur", "Ramanagara", "Chikmagalur", "Belthangady", "Karkala", "Puttur",
    "Sullia", "Sakleshpur", "Arsikere", "Tiptur", "Kundapura", "Sirsi", "Honnavar", "Ankola", "Dandeli",
    "Hubli", "Bhatkal", "Byndoor", "Ullal", "Mangalore", "Bantwal", "Moodbidri", "Mulki", "Kaup", "Udupi",
    "Karkala", "Padubidri", "Haliyal", "Supa", "Sirsi", "Mundgod", "Yellapur", "Ankola", "Karwar"
]


def validate_city(value):
        if len(value)>100:
            raise ValidationError("City name exceeded maximum limit.")
        if value.title() not in VALID_CITIES:
            raise ValidationError("Invalid city name. Please enter a valid city.")

















