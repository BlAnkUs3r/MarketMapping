import customtkinter
import os
import subprocess
import mapInterface as mp

sampleTuple = []
class routeViewButton(customtkinter.CTkButton):
    def __init__(self, master, start, end):
        print("Im here!")
        super().__init__(master, text="ViewRoute", command= lambda: self.showRoute(start,end))

    def showRoute(self, first, last):
        mp.drawAndShow(first,last)

with open("mapInfo.txt", "r") as file:
      for line in file:
            tup = line.strip().split(",  ")
            sampleTuple.append(tuple(tup))

root = customtkinter.CTk()
root.title("Market Mapping Map View")
root.geometry("{}x{}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.grid_columnconfigure(0, weight=3)
root.grid_rowconfigure(0, weight=1)

scrollableButtons = customtkinter.CTkScrollableFrame(root, label_text="Route List")
scrollableButtons.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

for i, value in enumerate(sampleTuple):
            if (i + 1) != len(sampleTuple):
                frame = customtkinter.CTkFrame(scrollableButtons)
                frame.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="nsew")
                frame.grid_columnconfigure(0, weight=1)

                newButton = routeViewButton(frame, sampleTuple[i][1], sampleTuple[i+1][1])
                print(sampleTuple[i][1] + " " + sampleTuple[i+1][1])
                newButton.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="e")

                ButtonText = customtkinter.CTkLabel(frame, text="Route From " + sampleTuple[i][0] + " (" + sampleTuple[i][1] + ")" " to " + sampleTuple[i+1][0] + " (" + sampleTuple[i+1][1] + ")" , fg_color="transparent", font=("roboto", 18))
                ButtonText.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
 

        

root.mainloop() 