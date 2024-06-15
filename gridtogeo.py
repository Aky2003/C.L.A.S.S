from geopy.geocoders import Nominatim

def addressleav(latitude, longitude):
    try:
        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.reverse((latitude, longitude), language="en")

        if location:
            address = location.address
            return address
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


