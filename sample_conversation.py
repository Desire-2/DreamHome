import json

# Sample real estate data
conversations = [
    ("What properties do you have available?", "We have a variety of properties available. Are you looking for something specific?"),
    ("Can you help me sell my house?", "Yes, we can help you with that. Please provide us with some details about your property."),
    ("Do you offer property management services?", "Yes, we provide professional property management services. Would you like to know more about it?"),
    ("I'm interested in renting an apartment.", "Great! We have several apartments available for rent. Could you please specify your requirements?"),
    ("What are the amenities included in the property?", "Our properties come with various amenities such as swimming pools, gyms, and parking facilities."),
    ("How can I schedule a property viewing?", "You can schedule a property viewing by contacting our office or filling out the online form on our website."),
    ("Are pets allowed in your rental properties?", "Yes, we allow pets in some of our rental properties. However, there may be restrictions and additional fees."),
    ("Can I get a mortgage through your agency?", "Yes, we work with several reputable lenders to help our clients secure mortgages at competitive rates."),
    ("What is the average price per square meter in the area?", "The average price per square meter varies depending on the location and type of property. We can provide you with a market analysis report for more accurate information."),
    ("How long does it usually take to sell a property?", "The time it takes to sell a property depends on various factors such as market conditions, pricing, and property features. We'll work closely with you to ensure a timely sale."),
    ("Do you offer assistance with property taxes?", "Yes, we can provide guidance on property taxes and connect you with tax professionals who can assist you further."),
    ("I'm looking for a commercial property for my business.", "Sure, we have a range of commercial properties available including office spaces, retail shops, and warehouses. Can you tell us more about your requirements?"),
    ("What is the process for buying a property?", "The buying process involves several steps including property search, negotiation, due diligence, and closing. Our experienced agents will guide you through each step."),
    ("Can I see more photos of the property?", "Certainly! We can provide you with additional photos and even schedule a virtual tour if you'd like."),
    ("Is there a homeowner association (HOA) fee for this property?", "Yes, some properties may have HOA fees to cover maintenance of common areas and amenities. We'll provide you with detailed information about any associated fees."),
    ("Are there any upcoming developments planned in the area?", "We stay updated on local developments and can provide you with information about upcoming projects that may impact property values."),
    ("I'm interested in investing in real estate. Can you help?", "Absolutely! Real estate investment can be a lucrative venture. We'll work with you to identify investment opportunities that align with your goals and preferences."),
    ("What are the financing options available for first-time homebuyers?", "There are various financing options available for first-time homebuyers including FHA loans, VA loans, and conventional mortgages. We can connect you with a mortgage specialist to explore your options."),
    # Add more conversations here
]

# Sample greetings
greetings = ["hi", "hello", "hey", "howdy", "greetings"]

# Create a dictionary to store the conversations and greetings
data = {
    "conversations": conversations,
    "greetings": greetings
}

# Save the data to a JSON file
with open('sample_data.json', 'w') as f:
    json.dump(data, f, indent=4)
