import tkinter as tk
import tkinter.ttk as ttk
from SmartHouseSystemDesktopCodeIoT import SmartSystem
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 
import matplotlib.pyplot 

class Smart_Home_System:
    def __init__(self, parentWindow):
        self.sh = SmartSystem()            # Create IoT interface object
        self.window = parentWindow
    #Create Widgets
        

        #Titles
        self.Title_Temperature=ttk.Label(self.window,text="Heating System",anchor="center",borderwidth=3,relief="ridge")
        self.Title_Lighting=ttk.Label(self.window,text="Lighting System",anchor="center",borderwidth=3,relief="ridge")
        #Heating 
        self.Is_Heating_Enabled = ttk.Checkbutton(self.window, text="Heating Enabled |",command=self.Enable_HCallback)
        self.Is_Heating_Enabled.invoke()
        self.Target_Temp_Label = ttk.Label(self.window, text="Target Temperature [C]:")    
        self.Target_Temp = ttk.Entry(self.window)
        self.Target_Temp.bind('<Key-Return>', self.Target_HCallback)  # Called when Return hit
        self.boilerOnLabel = ttk.Label(self.window, text="| Boiler state:")
        self.boilerOn = ttk.Label(self.window,text="       ")
        self.Actual_Temperature =ttk.Label(self.window,text=(f"Actual Temperature:{self.sh.actualTemperature} |"))
        
        
        #Lighting
        self.Is_Lighting_Enabled = ttk.Checkbutton(self.window, text="Lighting Enabled |",command=self.Enable_LCallback)
        self.Is_Lighting_Enabled.invoke()
        self.Threshold_Lighting_Label = ttk.Label(self.window, text="Threshold Lighting:")    
        self.Threshold_Ligthing = ttk.Entry(self.window)
        self.Threshold_Ligthing.bind('<Key-Return>', self.Target_LCallback)  # Called when Return hit
        self.LampOn_Label = ttk.Label(self.window, text="| Lamp State:")
        self.LampOn = ttk.Label(self.window,text="       ")
        self.Actual_LightLevel =ttk.Label(self.window,text=(f" Actual Light Level:{self.sh.ActualLighting} |"))
        
        
        
    #Widget location assignment
        self.Title_Temperature.grid(column = 0, row = 0, sticky='ew',columnspan=6)
        self.Title_Lighting.grid(column = 6, row = 0, sticky='ew',columnspan=6)
        #enabled settings
        self.Is_Heating_Enabled.grid(column=0,row=2,sticky='e')
        self.Is_Lighting_Enabled.grid(column=6,row=2,sticky='e')
        #temp settings
        self.Actual_Temperature.grid(column=1,row=2,sticky='ew')
        self.Target_Temp_Label.grid(column=2,row=2,sticky='ew')
        self.Target_Temp.grid(column=3,row=2,sticky='ew')
        #boiler settings
        self.boilerOnLabel.grid(column = 4, row = 2, sticky='ew')
        self.boilerOn.grid(column = 5, row = 2, sticky='ew')
        #Lighting settings
        self.Actual_LightLevel.grid(column=7,row=2,sticky='ew')
        self.Threshold_Lighting_Label.grid(column=8,row=2,sticky='ew')
        self.Threshold_Ligthing.grid(column=9,row=2,sticky='ew')
        self.LampOn_Label.grid(column = 10, row = 2, sticky='ew')
        self.LampOn.grid(column = 11, row = 2, sticky='ew')
        
        
        
        
        
    #Widget smoothness 
        self.window.columnconfigure(0, weight = 1)
        self.window.columnconfigure(6, weight = 1)
        self.window.rowconfigure(1, weight = 1)
        
        
        
        matplotlib.pyplot .style.use("dark_background")
        #Temperature Plot
        
        self.temp_fig = Figure(figsize=(4,3))
        self.temp_axes = self.temp_fig.add_subplot(111)
        self.temp_axes.set_xlabel("Time")
        self.temp_axes.set_ylabel("Temperature [C]")
        self.temp_canvas = FigureCanvasTkAgg(self.temp_fig, master=self.window)
        self.temp_canvas.get_tk_widget().grid(column=0, row=1, sticky="news", columnspan=6)

        
        
        #LightPlot
        self.light_fig = Figure(figsize=(4,3))
        self.light_axes = self.light_fig.add_subplot(111)
        self.light_axes.set_xlabel("Time")
        self.light_axes.set_ylabel("Light Level")
        self.light_canvas = FigureCanvasTkAgg(self.light_fig, master=self.window)
        self.light_canvas.get_tk_widget().grid(column=6, row=1, sticky="news", columnspan=6)
        
        self.window.after(1000, self.timerCallback)         # Called in 1seconds
#Enable callbacks
    def Enable_HCallback(self):
        #Heating
        self.sh.isHeatingEnabled = ('selected' in self.Is_Heating_Enabled.state())
        print("Checked Heating:",self.sh.isHeatingEnabled)            
    def Enable_LCallback(self):
        #Lighting
        self.sh.Is_Lighting_Enabled = ('selected' in self.Is_Lighting_Enabled.state())
        print("Checked Ligthing:",self.sh.Is_Lighting_Enabled)
        
#input callbacks

    def Target_HCallback(self, event):
        #Heating
        self.sh.Target_Temp = int(self.Target_Temp.get())
        print("Target Temp:",self.sh.Target_Temp)
    def Target_LCallback(self, event):
        #Lighting
        self.sh.Threshold_Ligthing = int(self.Threshold_Ligthing.get())
        print("Threshold Lighthing:",self.sh.Threshold_Ligthing)
    def timerCallback(self):
        self.sh.postData()                                  # Update IoT data...
        self.sh.updateFromIoT()
        self.boilerOn.config(text=str(self.sh.isBoilerOn))  # ...and update GUI
        self.LampOn.config(text=str(self.sh.LampOn))
        self.Actual_LightLevel.config(text=(f" Actual Light Level:{self.sh.ActualLighting} |"))
        self.Actual_Temperature.config(text=(f" Actual Temperature :{self.sh.actualTemperature} |"))
        matplotlib.pyplot .style.use("dark_background")
        #temp
        self.temp_axes.clear()
        self.temp_axes.grid(True)
        self.temp_axes.plot(self.sh.times, self.sh.temperatures, color="red")
        self.temp_axes.set_xlabel("Time")
        self.temp_axes.set_ylabel("Temperature [C]")
        self.temp_fig.autofmt_xdate()
        self.temp_canvas.draw()
        #Light
        self.light_axes.clear()
        self.light_axes.grid(True)
        self.light_axes.plot(self.sh.times, self.sh.LightLevels, color="orange")
        self.light_axes.set_xlabel("Time")
        self.light_axes.set_ylabel("Light Level")
        self.light_fig.autofmt_xdate()
        self.light_canvas.draw()




        self.window.after(1000, self.timerCallback)         # Call again in 1seconds






window = tk.Tk()
app = Smart_Home_System(window)
window.mainloop()

       