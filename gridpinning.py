import folium
import filenamegenerator
import foldercreator
def droppin(latitude, longitude):
    map_center = [latitude, longitude]
    my_map = folium.Map(location=map_center, 
                        zoom_start=15)
    folium.Marker(location=map_center, 
                  popup='Custom Marker').add_to(my_map)
    filename = filenamegenerator.filena(latitude,
                                        longitude)
    my_map.save(f"CASEOF_{filename}.html")
    print(f"Map saved to CASE_OF_{filename}.html")
    foldercreator.createfolder(filename)

    
