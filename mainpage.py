import customtkinter
import os
import subprocess
from PIL import Image

#current directory
current_directory = os.getcwd()

shoppingCart = []

def getShoppingCart():
    return shoppingCart

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Sets The Title of The Page and Allows You To Adjust Object Placement
        self.title("Market Mapping")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)


        #self.bottom_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        #self.bottom_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")
        #self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.top_frame = customtkinter.CTkFrame(self,fg_color="transparent")
        self.top_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        values = [("CVS (South Crouse)", "CVS.png"), ("Family Dollar (Onondaga Boulevard)", "FamilyDollar.png"), ("Target (Comstock Avenue)", "Target.png"), ("Wallgreens (University Ave)", "Walgreens.png"), ("Walmart (Walnut Pl)", "Walmart.png")]
        self.scrollable_checkbox_frame = StoreItemFrame(self, title="Store List", values=values)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")


        self.button = customtkinter.CTkButton(self.top_frame, text="Proceed To Map", command=self.openMap)
        self.button.grid(row=0, column=2, padx=10, pady=10)

        self.itemViewButton = customtkinter.CTkButton(self.top_frame, text="View Items", command=self.viewItemList)
        self.itemViewButton.grid(row = 0, column=1, padx=10, pady=10)

        self.logoutButton = customtkinter.CTkButton(self.top_frame, text="LogOut", command=self.logOut)
        self.logoutButton.grid(row=0, column=0, padx=10, pady=10)

        self.topWindow = None

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
            self.topWindow.geometry("200x200")
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
            checkbox = customtkinter.CTkCheckBox(self.scrollableItems, text=value)
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
            if checkbox.get() == 1:
                removeFromCart(checkbox.cget("text"))
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
            storeImage = customtkinter.CTkImage(light_image=Image.open(value[1]), size=(200,180))
            storeImageLabel = customtkinter.CTkLabel(frame, image=storeImage, text="")
            storeImageLabel.grid(row=0,column=0, padx=10, pady=(10,0), sticky="ew")

            #checkbox = customtkinter.CTkButton(frame, text="add To Cart", command= lambda: self.displayParam(value))
            #checkbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

            newButton = storeCartButton(frame, value[0])
            newButton.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="e")

            storeText = customtkinter.CTkLabel(frame, text=value[0], fg_color="transparent", font=("roboto", 18))
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
        shoppingCart.append(item)
        app.createConfirmationWindow("Item Added")       
    print(shoppingCart)

def removeFromCart(item):
    if item in shoppingCart:
        shoppingCart.remove(item)
    print(shoppingCart)

def getShoppingCart():
    return shoppingCart

def clearCart():
    shoppingCart.clear()

app = App()

app.mainloop()