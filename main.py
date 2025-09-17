
import pickle
from datetime import date
from graphics import *


Routes = {}
routesfile = "trips.txt"
shapeFile = "data/shapes.txt"
Shape = {}
Disruptions = []

def loadRoute():
    '''
    purpose: Loads the route data from a file and stores it in a dictionary that is keyed by the route_id
    parameters: None
    return: Routes
    '''
    try:
        file = input("Enter a filename : ")
        if file == "":
            file = "data/trips.txt"
        filen = file
        with open(file, "r") as file:
            lines = file.read().splitlines()
        
        lines.pop(0)

        for i in lines:
            line = i.strip().split(",")
            key = line[0]  # Route ID
            shape_id = line[6]  # Shape ID
            destination = line[3]  # Route Destination

            # If route is already in dictionary, append new shape ID (prevent duplicates)
            if key in Routes:
                if shape_id not in Routes[key][0]:  
                    Routes[key][0].add(shape_id)  # Adds shape ID to the set
            else:
                Routes[key] = [set([shape_id]), destination]  # Store shape IDs as a set

        print(f"Data from {filen} loaded\n")
        main()
        return Routes

    except FileNotFoundError:
        print(f"IOError : Couldn't open {file}\n")
        main()

def loadShapes():
    '''
    purpose: Loads the Shape data from a file and stores it in a dictionary that is keyed by the shape_id
    parameters: None
    return: Shape
    '''
    try:
        file = input("Enter a filename : ")
        if file == "":
            file = "data/shapes.txt"
        filen = file
        with open(file, "r") as file:
            lines = file.read().splitlines()
        lines.pop(0)
        for i in lines:
            line = i.strip().split(",")
            shapekey = line[0]
            lat = float(line[1])
            lon = float(line[2])

            if shapekey not in Shape:
                Shape[shapekey] = []

            Shape[shapekey].append((lat, lon))
        print(f"Data from {filen} loaded\n")
        main()
        return Shape
    except FileNotFoundError:
        print(f"IOError : Couldn't open {file}\n")
        main()


def printShapes():
    route_input = input("Enter route: ").strip()

    if not Routes:
        print("Route data hasn't been loaded yet.")
        main()
        return

    if route_input in Routes:
        shape_ids = Routes[route_input][0]
    else:
        print(f"Route {route_input} not found.")
        main()
        return

    route_name = None
    try:
        with open("data/routes.txt", "r") as file:
            lines = file.read().splitlines()

        for line in lines[1:]:
            parts = line.split(",")
            if parts[0].strip() == route_input:
                route_name = parts[3].strip().strip('"')
                break

    except FileNotFoundError:
        print("IOError: Couldn't open data/routes.txt")
        main()
        return

    if route_name is None:
        print("** NOT FOUND **")
        main()
        return

    if shape_ids:
        print(f"Shape IDs for route [{route_name}]:")
        for sid in sorted(shape_ids):
            print(f"  {sid}")
    else:
        print(f"No shape IDs found for route {route_input}.")
        main()
    main()


def printCoordinates():
    '''
    purpose: Prints all the coordinates in pairs that are listed under the shape; can be quite large
    parameters: None
    return: None
    '''
    if len(Shape) < 1:
        print("Shape data hasn't been loaded yet")
        return
    shape_id = input("Enter a shape_id: ").strip()
    print(shape_id)
    if shape_id in Shape:
        print("Coordinates are: ")
        for lat, lon in Shape[shape_id]:
            print(f"({lat:.6f}, {lon:.6f})")    
    else:
        print("** NOT FOUND **")
        main()
    main()
    

def load_disruptions():
    '''
    purpose: Fills a list with the tuples of the fisnish dates of disruptions and
    a correspoinding tuple with the coordinates
    parameters: None
    return: Disruptions
    '''
    global Disruptions
    Disruptions = [] 

    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
              "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

    try:
        file_name = input("Enter a filename: ").strip()
        if not file_name:
            file_name = "data/traffic_disruptions.txt"
        
        with open(file_name, "r") as file:
            lines = file.read().splitlines()
        
        lines.pop(0)  # Remove header row
        
        for line in lines:
            parts = line.split(",")
            
            # Parse the finish date
            month, day = parts[5].strip('"').split()
            month = months[month]  # Convert month name to number
            day = int(day.replace(",", ""))
            year = int(parts[6].strip('"').strip()) 
            finish_date = date(year, month, day)  # Create date object
            
            # Parse the coordinates
            point_str = parts[-1].strip().replace("POINT (", "").replace(")", "")
            lon, lat = point_str.split()
            lat, lon = float(lat), float(lon)                   

            # Store the data
            Disruptions.append((finish_date, (lat, lon)))
        
        print(f"Data from {file_name} loaded\n")
        main()
        return Disruptions

    except FileNotFoundError:
        print(f"IOError: Couldn't open {file_name}\n")
        main()

def longestRoute():
    '''
    purpose: Prints the longest shape in terms of coordinates and its amount of coords(count)
    parameters: None
    return: None
    '''
    routeShapes = []
    route_input = input("Enter route: ").strip()

    if not Routes:
        print("Route data hasn't been loaded yet.")
        main()
        return

    if route_input in Routes:
        shape_ids = Routes[route_input][0]
    else:
        print("** NOT FOUND **")
        main()
        return
    
    if shape_ids:
        length = 0
        lenghtSaved = 0
        savedShape = ""
        for sid in sorted(shape_ids):
            routeShapes.append(sid) #save all routes
        for i in routeShapes:
            length = len(Shape[i])
            if lenghtSaved < length:
                lenghtSaved = length #save longest length
                savedShape = i #save the longest route
        print(f"The longest shape for {route_input} is {savedShape} with {lenghtSaved} coordinates")

    else:
        print(f"No shape IDs found for route {route_input}.")
        main()
    main()



def pickleSave():
    '''
    purpose: Saves Routes,Shape,Disruptions to a pickle file
    parameters: None
    return: None
    '''
    try:
        file = input("Enter a filename : ")
        if file == "":
            file = "data/etsdata.p"
        with open(file, "wb") as f:
            pickle.dump({"Routes": Routes, "Shapes": Shape, "Disruptions": Disruptions}, f)
        print(f"Data structures successfully written to {file}")
        main()
    except FileNotFoundError:
        print("IOError: Couldn't open file")
        main()


def pickLoad():
    '''
    purpose: Loads Routes, Shape, Disruptions to a pickle file
    parameters: None
    return: None
    '''
    global Routes, Shape, Disruptions
    
    Routes, Shape, Disruptions = {}, {}, []  # Reset in case loading fails
   
    try:
        file = input("Enter a filename : ")
        if file == "":
            file = "data/etsdata.p"
        with open(file, "rb") as f:
            data = pickle.load(f)
            Routes = data["Routes"]
            Shape = data["Shapes"]
            Disruptions = data["Disruptions"]
        print(f"Routes, shapes and disruptions Data structures successfully loaded from {file}")
        main()
        return Routes,Shape,Disruptions
    except FileNotFoundError:
        print("IOError: Couldn't open file")
        main()
        
        
def interactive_map():
    '''
    purpose: Creates an interactive map that displays the longest ETS routes and disruptions on a background map.
    parameters: None
    return: None
    '''
    global Routes, Shape, Disruptions
    win = GraphWin("ETS Data", 800, 920)
    win.setCoords(-113.720049, 53.393703, -113.320418, 53.657116)
   
    center_lon = (-113.720049 + -113.320418) / 2
    center_lat = (53.393703 + 53.657116) / 2
    bg = Image(Point(center_lon, center_lat), "edmonton.png")
    bg.draw(win)  
        
    from_label = Text(Point(-113.70, 53.65), "From:")
    from_label.setSize(12) #set text size
    from_label.setStyle("bold") #bold text
    from_label.draw(win)
    from_entry = Entry(Point(-113.66, 53.65), 12)
    from_entry.setFill("white")
    from_entry.draw(win)

    to_label = Text(Point(-113.70, 53.64), "To:")
    to_label.setSize(12)
    to_label.setStyle("bold")
    to_label.draw(win)
    to_entry = Entry(Point(-113.66, 53.64), 12)
    to_entry.setFill("white")
    to_entry.draw(win)
    
    #feedback = Text(Point(( -113.720049 + -113.320418)/2, 53.625), "")
    feedback = Text(Point(center_lon - 0.11, 53.61), "") #center_lon - 0.11 a larger number moves the text more to the left
    feedback.setSize(14)
    feedback.setStyle("bold")
    feedback.draw(win)

    search_button = Rectangle(Point(-113.71, 53.63), Point(-113.67, 53.62))
    search_button.setFill("Tan")
    search_button.draw(win)
    search_text = Text(search_button.getCenter(), "Search")
    search_text.draw(win)

    clear_button = Rectangle(Point(-113.66, 53.63), Point(-113.62, 53.62))
    clear_button.setFill("Tan")
    clear_button.draw(win)
    clear_text = Text(clear_button.getCenter(), "Clear")
    clear_text.draw(win)
    
    search_ll = search_button.getP1() # lower-left for Search
    search_ur = search_button.getP2() # upper-right for Search
    clear_ll = clear_button.getP1() # lower-left for Clear
    clear_ur = clear_button.getP2() # upper-right for Clear    
    
    today = date.today()
    disruption_radius = 0.0005 #Red dots on map
    for finish_date, (lat, lon) in Disruptions:
        if finish_date > today:
            circ = Circle(Point(lon, lat), disruption_radius)
            circ.setFill("red")
            circ.setOutline("red")
            circ.draw(win)
    
    route_drawings = []    
    
    while True:
        try:
            click_pt = win.getMouse()
        except GraphicsError:
            break
        if (search_ll.getX() <= click_pt.getX() <= search_ur.getX() and 
            search_ur.getY() <= click_pt.getY() <= search_ll.getY()):  #Checks if search button was clicked      
            frm = from_entry.getText().strip().lower() #Gets input from the text boxes
            to_ = to_entry.getText().strip().lower()
            if not (frm or to_):
                feedback.setText("Please enter at least one location.")
            else:
                with open("data/routes.txt", "r") as f:
                    lines = f.read().splitlines()[1:]
                found_route_id = None
                found_route_name = None
                for line in lines:  #Loops through each route to find a match
                    parts = line.split(",")
                    route_id = parts[0].strip()
                    route_name = parts[3].strip().strip('"')
                    parts_route = route_name.split("-")
                    if len(parts_route) == 1: #Get route names for point and destination
                        start = parts_route[0].strip().lower()
                        end = start
                    else:
                        start = parts_route[0].strip().lower()
                        end = parts_route[-1].strip().lower()
                    if frm and to_:
                        if start == frm and end == to_:
                            found_route_id = route_id
                            found_route_name = route_name
                            break
                    elif frm:
                        if start == frm or end == frm:
                            found_route_id = route_id
                            found_route_name = route_name
                            break
                    elif to_:
                        if start == to_ or end == to_:
                            found_route_id = route_id
                            found_route_name = route_name
                            break
                if not found_route_id:
                    feedback.setText("NOT FOUND")
                else:
                    shape_ids = Routes[found_route_id][0]
                    longest = None
                    max_length = 0
                    for sid in shape_ids:
                        if sid in Shape:
                            l = len(Shape[sid])
                            if l > max_length:
                                max_length = l
                                longest = sid
                    if longest:
                        coords = Shape[longest]
                        for i in range(len(coords) - 1):
                            lat1, lon1 = coords[i]
                            lat2, lon2 = coords[i + 1]
                            seg = Line(Point(lon1, lat1), Point(lon2, lat2))
                            seg.setFill("blue")
                            seg.setWidth(2)
                            seg.draw(win)
                            route_drawings.append(seg)
                        feedback.setText(f"Drawing route {found_route_id}")
                    else:
                        feedback.setText("No shape coordinates found.")
        elif (clear_ll.getX() <= click_pt.getX() <= clear_ur.getX() and 
              clear_ur.getY() <= click_pt.getY() <= clear_ll.getY()): # Check if clear button was clicked      
            from_entry.setText("")
            to_entry.setText("")
            feedback.setText("")

    
    win.close()

def main():
    '''
    purpose: displays the menu in console
    parameters: None
    return: None
    '''    
    print(f"Edmonton Transit System\n---------------------------------\n(1) Load route data\n(2) Load shapes data\n(3) Load disruptions data\n\n(4) Print shape IDs for a route\n(5) Print coordinates for a shape ID\n(6) Find longest shape for route\n\n(7) Save routes, shapes and disruptions in a pickle\n(8) Load routes, shapes and disruptions from a pickle\n\n(9) Interactive map\n(0) Quit\n")
    inputCommand()


def inputCommand():
    '''
    purpose: Handles the inputs in the console and calls the correct function.
    parameters: None
    return: None
    '''    
    command = input("Enter Command : ")
    if not command.isdigit() or int(command) > 9:
        print("Invalid Option\n")
        main()
    elif int(command) == 1:
        loadRoute()
    elif int(command) == 2:
        loadShapes()
    elif int(command) == 3:
        load_disruptions()
    elif int(command) == 4:
        printShapes()
    elif int(command) == 5:
        printCoordinates()
    elif int(command) == 6:
        longestRoute()
    elif int(command) == 7:
        pickleSave()
    elif int(command) == 8:
        pickLoad()
    elif int(command) == 9:
        interactive_map()
        main()
    elif int(command) == 0:
        quit()


if __name__ == "__main__":
    main()