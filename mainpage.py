import customtkinter
import os
import subprocess
import apiInterface as call
from PIL import Image
import requests

#current directory
current_directory = os.getcwd()

shoppingCart = []


itemData = []


def getShoppingCart():
    return shoppingCart

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Sets The Title of The Page and Allows You To Adjust Object Placement
        self.title("Market Mapping")
        self.geometry("720x720")
        self.grid_columnconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.userLocation = ''
        #self.bottom_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        #self.bottom_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")
        #self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.top_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        
        self.top_frame.grid_columnconfigure(1, weight=2)
        self.top_frame.grid_columnconfigure(2, weight=1)
        self.top_frame.grid_columnconfigure(3, weight=2)
    


        self.values = []
        self.scrollable_checkbox_frame = StoreItemFrame(self, title="Store List", values=self.values)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")


        self.button = customtkinter.CTkButton(self.top_frame, text="Proceed To Map", command=self.openMap)
        self.button.grid(row=0, column=4, padx=10, pady=10)

        self.LocationButton = customtkinter.CTkButton(self.top_frame, text="Change Location", command=self.openLocationChange)
        self.LocationButton.grid(row=0, column=2, padx=10, pady=10)

        self.itemViewButton = customtkinter.CTkButton(self.top_frame, text="View Items", command=self.viewItemList)
        self.itemViewButton.grid(row = 0, column=3, padx=10, pady=10)

        self.searchButton = customtkinter.CTkButton(self.top_frame,text="Search", command=self.openSearch)
        self.searchButton.grid(row = 0, column=1, padx=10, pady=10)

        self.logoutButton = customtkinter.CTkButton(self.top_frame, text="LogOut", command=self.logOut)
        self.logoutButton.grid(row=0, column=0, padx=10, pady=10)

        self.topWindow = None


    def openLocationChange(self):
        # Open a pop up window with a text box for the user to input a location
        # If the text box is empty display pop up telling user the location is empty without destroying top level window (either that or display the error in the window itself)
        # Upon the button being pressed with a location, the api call is made and the items are rendered
        # If there is an invalid location error say that in a pop up window and display no items

        if self.topWindow is not None:
            self.topWindow.destroy()

        self.topWindow = customtkinter.CTkToplevel(self)
        self.topWindow.geometry("500x500")
        self.topWindow.grid_columnconfigure(0, weight=1)
        self.topWindow.grid_columnconfigure(1, weight=1)
        label = customtkinter.CTkLabel(self.topWindow, text="Please input your location (Address Prefered)", font=("roboto", 20))
        label.grid(row=0, column=0, padx=10, pady=10)

        entryField = customtkinter.CTkEntry(self.topWindow, placeholder_text="Input Location Here", width=200)
        entryField.grid(row=1, column=0, padx=10, pady=10)

        finalizeButton = customtkinter.CTkButton(self.topWindow, text="Set Location",command= lambda: self.setLocationSearch(entryField.get()))
        finalizeButton.grid(row=2, column=0, padx=10, pady=10)

        self.topWindow.after(100, self.topWindow.lift)

    def openSearch(self):
        if self.topWindow is not None:
            self.topWindow.destroy()

        self.topWindow = customtkinter.CTkToplevel(self)
        self.topWindow.geometry("500x500")
        self.topWindow.grid_columnconfigure(0, weight=1)
        self.topWindow.grid_columnconfigure(2, weight=1)
        label = customtkinter.CTkLabel(self.topWindow, text="Please Input Store Name or Search Term", font=("roboto", 20))
        label.grid(row=0, column=0, padx=10, pady=10)

        label2 = customtkinter.CTkLabel(self.topWindow, text="(Leave Blank For Default Search of Nearby Stores)", font=("roboto", 20))
        label2.grid(row=1, column=0, padx=10, pady=10)

        entryField = customtkinter.CTkEntry(self.topWindow, placeholder_text="Input Store Name Here", width=200)
        entryField.grid(row=2, column=0, padx=10, pady=10)

        finalizeButton = customtkinter.CTkButton(self.topWindow, text="Search For Stores",command= lambda: self.storeSearch(entryField.get()))
        finalizeButton.grid(row=3, column=0, padx=10, pady=10)

        self.topWindow.after(100, self.topWindow.lift)
    

    def storeSearch(self, searchTerm):
        if self.userLocation == '':
            self.createConfirmationWindow("Cannot Search With Empty Location!")
        else:
            itemData = setItemsWithSearch(self.userLocation, searchTerm)
            self.renderItems(itemData)

    def setLocationSearch(self, location):
        # Check if Location Field is Empty, if so display pop up saying the location is empty
        # Other Function should also ouput error if location dada is invalid
        if location == '':
            self.createConfirmationWindow("Location Cannot be Empty!")
        else:
            self.userLocation = location
            itemData = setItemsNoSearch(self.userLocation)
            self.renderItems(itemData)
            clearCart()


    def renderItems(self, values):
        self.values = values
        self.scrollable_checkbox_frame = StoreItemFrame(self, title="Store List", values=self.values)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")


    def getTopWindow(self):
        return self.topWindow
    
    def setTopWindow(self, val):
        self.topWindow = val

    def createConfirmationWindow(self, text):
        #This Creates A Window Verifying To The User That An Item Has Been Added
        if self.topWindow is None or not self.topWindow.winfo_exists():    
            self.topWindow = customtkinter.CTkToplevel(self)
            self.topWindow.geometry("200x200")
            topWindowLabel = customtkinter.CTkLabel(self.topWindow, text=text)
            topWindowLabel.pack(side="top", padx=20, pady=20)
            #Ensures The Top Window Appears At Front of App
            self.topWindow.after(20, self.topWindow.lift)
        else:
            #If There Is Already A Top Window, The Old One Is Destroyed and Replaced With The New
            self.topWindow.destroy()
            self.topWindow = customtkinter.CTkToplevel(self)
            self.topWindow.geometry("250x200")
            topWindowLabel = customtkinter.CTkLabel(self.topWindow, text=text)
            topWindowLabel.pack(side="top", padx=20, pady=20)
            self.topWindow.after(20, self.topWindow.lift)

    def openMap(self):
    # Specify the path to the map.py script here
        map_script_path = os.path.join(current_directory, "map.py")
        # Close the current UI window
        self.destroy()
        try:
            # Start the map.py script and wait for it to complete
            subprocess.run(["python", map_script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running map.py: {e}")

    def logOut(self):
     # Specify the path to the map.py script here
        UI_script_path = os.path.join(current_directory, "UI.py")
        # Close the current UI window
        self.destroy()
        try:
            # Start the map.py script and wait for it to complete
            subprocess.run(["python", UI_script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running map.py: {e}")   

    def viewItemList(self):
        if self.topWindow is None or not self.topWindow.winfo_exists():    
            self.topWindow = itemList(self)
        else:
            self.topWindow.destroy()
            self.topWindow = itemList(self)



        
        
class itemList(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x400")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.after(20, self.lift)

        self.scrollableItems = customtkinter.CTkScrollableFrame(self, label_text= "Items On Map")
        self.scrollableItems.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.bottom_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.bottom_frame.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="nsew")
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        self.clearButton = customtkinter.CTkButton(self.bottom_frame, text="Clear All", command=self.clearItems)
        self.clearButton.grid(row=0, column=2,  padx=10, pady=(0, 10), sticky="sw")

        self.deleteItems = customtkinter.CTkButton(self.bottom_frame, text="Delete Selected Items", command=self.destroySelectedItems)
        self.deleteItems.grid(row=0, column=0,  padx=10, pady=(0, 10), sticky="se")

        self.checkboxes = []
        self.renderItems()


    def renderItems(self):
        for i, value in enumerate(getShoppingCart()):
            checkbox = customtkinter.CTkCheckBox(self.scrollableItems, text=value[0] + " (" + value[1] + ")", onvalue=value[0] + ",  " + value[1], offvalue=0)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)
    
    def destroyItems(self):
        for i in self.checkboxes:
            i.destroy()

    def clearItems(self):
        clearCart()
        self.destroyItems()
        self.renderItems()
    
    def destroySelectedItems(self):
        for checkbox in self.checkboxes:
            if checkbox.get() != 0:
                delim = checkbox.cget("onvalue").split(',  ')
                removeFromCart(tuple(delim))
        self.destroyItems()
        self.renderItems()
        
    

        
        

class StoreItemFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            frame = customtkinter.CTkFrame(self)
            frame.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)

            #Add Image

            storeImage = customtkinter.CTkImage(light_image=Image.open(requests.get(value[2], stream=True).raw), size=(200,180))
            storeImageLabel = customtkinter.CTkLabel(frame, image=storeImage, text="")
            storeImageLabel.grid(row=0,column=0, padx=10, pady=(10,0), sticky="ew")

            #checkbox = customtkinter.CTkButton(frame, text="add To Cart", command= lambda: self.displayParam(value))
            #checkbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

            newButton = storeCartButton(frame, (value[0], value[1]))
            newButton.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="e")

            storeText = customtkinter.CTkLabel(frame, text=value[0] + " (" + value[1] + ")", fg_color="transparent", font=("roboto", 18))
            storeText.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

            self.checkboxes.append(frame)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class storeCartButton(customtkinter.CTkButton):
    def __init__(self, master, value):
        super().__init__(master, text="Add To Map", command= lambda: self.displayParam(value))

    def displayParam(self, val):
        addToCart(val)


def addToCart(item):
    if item in shoppingCart:
        app.createConfirmationWindow("Item Already Exists")
    else:
        if len(shoppingCart) == 10:
            app.createConfirmationWindow("Too Many Items In Cart! (Limit 10)")
        else:
            shoppingCart.append(item)
            app.createConfirmationWindow("Item Added")       

def removeFromCart(item):
    if item in shoppingCart:
        shoppingCart.remove(item)

def getShoppingCart():
    return shoppingCart

def clearCart():
    shoppingCart.clear()



app = App()

def setItemsNoSearch(location):
    # This is the default set method run when the app starts up or when the user searches with an empty text box
    # item list should be a list of tuples, each tuple having a name, address and image url
    # if the image url for a store is empty skip it
    info = call.getStoreInfoNoSearch(location)
    if 'error' in info.keys():
        app.createConfirmationWindow("ERROR: Location is Invalid")
        return []
    else:

        itemList = []

        for store in info['businesses']:
            if store['image_url'] != '' and store['location']['address1'][0].isdigit():
                information = (store['name'], store['location']['address1'], store['image_url'])
                itemList.append(information)

        return itemList
    
def setItemsWithSearch(location, search):
    info = call.getStoreInfoWithSearch(location, search)
    if 'error' in info.keys():
        app.createConfirmationWindow("ERROR: Location is Invalid")
        return []
    else:

        itemList = []

        for store in info['businesses']:
            if store['image_url'] != '' and store['location']['address1'][0].isdigit():
                information = (store['name'], store['location']['address1'], store['image_url'])
                itemList.append(information)

        return itemList



#app.renderItems([("CVS (South Crouse)", "CVS.png"), ("Family Dollar (Onondaga Boulevard)", "FamilyDollar.png"), ("Target (Comstock Avenue)", "Target.png"), ("Wallgreens (University Ave)", "Walgreens.png"), ("Walmart (Walnut Pl)", "Walmart.png")])


app.openLocationChange()
app.mainloop()