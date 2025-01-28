
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
import requests

class DisplayWindow(QWidget):
    def __init__(self, captured_pokemons):
        super().__init__()
        self.w = None        
        self.setFixedSize(650, 400)

        next_button = QPushButton("NExt",self)
        next_button.setGeometry(25,175,80,20)
        
        

       

class SearchWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
       
        self.w = None        
        self.setFixedSize(850, 500)
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20) 
        self.textbox.setGeometry(50, 50, 280, 40)
        label1 = QLabel("Enter the name", self)
        label1.setGeometry(50, 5, 600, 70)

        enter_button = QPushButton("Search", self)
        enter_button.setGeometry(50, 300, 160, 43)
        enter_button.clicked.connect(self.pokemon_data)

        capture_button = QPushButton("Capture", self)
        capture_button.setGeometry(50, 350, 160, 43)
        capture_button.clicked.connect(self.capture_pokemon)

        display_button = QPushButton("Display", self)
        display_button.setGeometry(50, 400, 160, 43)
        display_button.clicked.connect(self.capture_window)

        self.pokemon_details = QLabel(self)
        self.pokemon_details.setGeometry(50, 100, 300, 200)
        self.pokemon_details.setWordWrap(True)

        self.pokemon_image = QLabel(self)
        self.pokemon_image.setGeometry(400, 50, 200, 200)
        self.pokemon_image.setScaledContents(True)

    ## TO-DO ##

    # 1 #
    # Fetch the data from from the API.
    # Display the name, official artwork (image), abilities, types and stats when queried with a Pokémon name.
    # Add the background provided in assets
     #API to fetch data
       

    # 2 #
    # Capture the Pokémon i.e. download the image.

    # 3 #
    # Display all the Pokémon captured with their respective names using a new window.
        self.poke_data = {}
        self.poke_img = {}
        self.captured_pokemons=[]
    def pokemon_data(self):
                poke_name = self.textbox.text().strip().lower()
                if not poke_name:
                    self.pokemon_details.setText("Please enter a Pokémon name.")
                    return
                url=f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    self.poke_data = {
                        "name": data['name'],
                        "abilities": [ability['ability']['name'] for ability in data['abilities']],
                        "types": [poke_type['type']['name'] for poke_type in data['types']],
                        "stats": {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
                        "image": data['sprites']['front_default']
                    }
                        # Display Pokémon data
                    self.display_pokemon_data()
                else:
                    self.pokemon_details.setText("Pokémon not found. Please check the name and try again.")

    def display_pokemon_data(self):
        """
        Display Pokémon data including name, abilities, types, stats, and image.
        """
        details = f"Name: {self.poke_data['name']}\n"
        details += f"Abilities: {', '.join(self.poke_data['abilities'])}\n"
        details += f"Types: {', '.join(self.poke_data['types'])}\n"
        details += "Stats:\n"
        for stat, value in self.poke_data['stats'].items():
            details += f"  {stat}: {value}\n"

        self.pokemon_details.setText(details)

        # Load and display Pokémon image
        if self.poke_data['image']:
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(self.poke_data['image']).content)
            self.pokemon_image.setPixmap(pixmap)
    def capture_pokemon(self):  
        # Capture the currently displayed Pokémon  
        current_pokemon = self.textbox.text().strip().lower()  
        if current_pokemon and current_pokemon not in self.captured_pokemons:  
            self.captured_pokemons.append(current_pokemon)  # Add to captured list
            QMessageBox.information(self, "Captured", f"{current_pokemon.capitalize()} has been captured!")  

        else:  
            QMessageBox.warning(self, "Warning", "Pokémon already captured or invalid name.")
    
    def capture_window(self, checked):
        if self.w is None:
            self.w = DisplayWindow(self.captured_pokemons)
        self.w.show()

      
    

  
                          

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SearchWindow()
    window.show()
    sys.exit(app.exec())
