from app import app, db, Property, Agent
# Define a function to add sample properties and agents
def add_sample_properties():
    with app.app_context():
        # Create sample agents
        agent1 = Agent(name='John Doe', email='john@example1.com', phone='123-456-7890')
        agent2 = Agent(name='Jane Smith', email='jane@example1.com', phone='987-654-3210')
        agent3 = Agent(name='Desire Bikorimana', email='bikorimanadesire@yahoo.com', phone='250-780-784924')

        # Add agents to the session
        db.session.add(agent1)
        db.session.add(agent2)
        db.session.add(agent3)
        db.session.commit()

        # Create sample properties
        property1 = Property(
            title='Beautiful Apartment in the City Center',
            description='Spacious apartment with modern amenities',
            price=250000,
            num_bedrooms=2,
            num_bathrooms=2,
            area=120.5,
            location='City Center, New York',
            image_url='https://www.bing.com/images/search?view=detailV2&ccid=odSm%2bLqc&id=0D2D5AEA779D5042B23A0FFB827AC30932190576&thid=OIP.odSm-Lqc9Au-acbkdUboowHaE-&mediaurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.a1d4a6f8ba9cf40bbe69c6e47546e8a3%3frik%3ddgUZMgnDeoL7Dw%26riu%3dhttp%253a%252f%252fwww.luxxu.net%252fblog%252fwp-content%252fuploads%252f2017%252f02%252f20-Incredible-Modern-Houses-Around-the-United-States-5.jpg%26ehk%3djltOlopAEXlYw25Qjcb6BhHSadJcIyJ863PI4ffrO70%253d%26risl%3d1%26pid%3dImgRaw%26r%3d0&exph=2400&expw=3569&q=houses&simid=608016560614624697&FORM=IRPRST&ck=73BDD16A7D4CE80F3CD20BA2CA1418D9&selectedIndex=0&itb=0',
            year_built=2018,
            property_type='Apartment',
            amenities='Swimming pool, Gym, Parking',
            agent_id=agent1.id
        )

        property2 = Property(
            title='Luxury Villa with Ocean View',
            description='Stunning villa overlooking the ocean',
            price=1000000,
            num_bedrooms=4,
            num_bathrooms=3,
            area=300.0,
            location='Beachfront, Miami',
            image_url='https://www.bing.com/images/search?view=detailV2&ccid=nZZPg0Yq&id=2B7DCB542FF89AA6850301B0EA63E74D0001C1F6&thid=OIP.nZZPg0YqXs5cCd5xVXhyKgHaE8&mediaurl=https%3a%2f%2fs3.amazonaws.com%2fhomestratosphere%2fwp-content%2fuploads%2f2016%2f06%2f07101922%2f19ad-Northwest.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.9d964f83462a5ece5c09de715578722a%3frik%3d9sEBAE3nY%252bqwAQ%26pid%3dImgRaw%26r%3d0&exph=2912&expw=4368&q=houses&simid=607988969777736161&FORM=IRPRST&ck=FD2B581F1FFF9BF2743F58BCA11D9072&selectedIndex=3&itb=0',
            year_built=2015,
            property_type='Villa',
            amenities='Private beach access, Jacuzzi, Garden',
            agent_id=agent2.id
        )

        property3 = Property( 
            title='Luxury Apartment', description='Spacious apartment with great amenities', price=200000,
            num_bedrooms=3, num_bathrooms=2, area=150, location='City Center', image_url='apartment.jpg',
            year_built=2015, property_type='Apartment', amenities='Swimming pool, Gym', is_featured=True,
            is_for_sale=True, is_for_rent=False, agent_id=agent1.id)

        property4 =  Property(
            title='Cozy House', description='Charming house with a beautiful garden', price=300000,
            num_bedrooms=4, num_bathrooms=3, area=200, location='Suburb', image_url='house.jpg',
            year_built=2000, property_type='House', amenities='Garden, Garage', is_featured=True,
            is_for_sale=True, is_for_rent=False, agent_id=agent1.id)
        # Add more sample properties as needed

        # Add properties to the session
        db.session.add(property1)
        db.session.add(property2)
        db.session.add(property3)
        db.session.add(property4)
        db.session.commit()

# Call the function to add sample properties
add_sample_properties()
