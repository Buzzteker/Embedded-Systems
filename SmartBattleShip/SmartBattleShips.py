

###Aurthor:Bartosz Baranek
###Date Last Modifed:01/01/2026

###Description:
###			This program is to automatically guess a N*N sized board, with the minimum size N=8,
###         the program has a fallback of randomly guessing in a specific pattern to ensure continuious operation.
###         The main program consists of waiting untill a Hit has been registered, before constructing a heat map around the Hit ship and guessing the highest probability cell.							###



#This program requires the BattleShips python file
#For this program i have chosen to import the Random and Numpy modules to make calculating the next best guess easier
import random
import BattleShips
import numpy



class SmartBattleShips(BattleShips.BattleShips):
    def guess(self):
###################################################################################################################################################################################
###														program blow excludes all adjacent cells around a know ship

        ###blow the program convolves a pattern around a know ship, and sets those values into a '*', to show that they are garanteed to be empty 6
        #pattern to set all cells adjacent to a ship cell to a true value
        Proximity_Pattern=numpy.array([[True,True,True],
                                      [True,False,True],
                                      [True,True,True]])
        #generates a bolean array where any Y,X,B,A string gets converted to True, and the rest get converted to False                        
        P_Contains_Ship = numpy.isin(self.map,['Y','X','B','A'])
        #correlates the pattern to any True value in the P_contains_Ship array, and the resulting array will have the Original True from P_Contains_Ship outlined with a layer of True values
        Proximity_Location=BattleShips.correlate(P_Contains_Ship,Proximity_Pattern)

        if (self.map[Proximity_Location]==' ').any():
            self.map[Proximity_Location& (self.map==' ')]='*'

        
        
        
###################################################################################################################################################################################
###														Heat Map probability when hit


    
        if 'H' in self.map:# checks if theres a hit ship
            ###The arrays below are the pattern for all the possible ships that the board can place
            ###These arrays will be used to determine all possible placements and orientations that they can be in to create a HeatMap
            #Y-wing pattern
            YWing=numpy.array([
                                                    [0,1,0],
                                                    [1,1,1],
                                                    [1,0,1]])
            #X-wing pattern
            XWing=numpy.array([
                                                    [0,1,0],
                                                    [1,1,1],
                                                    [0,0,0]])
            #B-wing pattern
            BWing=numpy.array([
                                                    [0,1,0],
                                                    [0,1,0],
                                                    [0,1,0]])
            #A-wing pattern
            AWing=numpy.array([
                                                    [0,1,1],
                                                    [0,1,0],
                                                    [0,0,0]])
            


            #Sets all the ship patterns into a single array so i can cycle through the array inside a loop
            XYBA=[YWing,XWing,BWing,AWing]
            #Stores and converts the map into the HitMap variable so i can use it later on in the program
            HitMap=numpy.array(self.map)


            #the Hit_Pattern variable is a array that will be used to find all Hit cells and set them to True
            Hit_Pattern=numpy.array([[False,False,False],
                                    [False,True,False],
                                    [False,False,False]])
            #Contain_Hit checks the HitMap array for any cells with a H (indicates a hit) and converts them to true
            Contains_Hit = numpy.isin(HitMap,['H'])
#             print(Contains_Hit)

            ###Below is a series of code that converts the map into a integer and also setting all letter into negative numbers
            #stores the Map into a variable called m
            m=numpy.array(self.map)
            m[m=='H']=10
            m[m==' ']=0
            m[m=='/']=1
            m[m=='X']=1
            m[m=='B']=1
            m[m=='Y']=1
            m[m=='A']=1
            m[m=='*']=1
            # converts the m array into a integer array
            m=m.astype(int)
            #sets all 1 inside the m array into  a negative number
            m[m=='1']=-1000
            #stores the m array into the Hit_Heat_Map array so i can be used to continuiously add numbers together in each cell later on in the code
            Hit_Heat_Map=m

            ###Below is the main program to create a Heat map for the map
            ###the for loop is needed to check all 4 directions of rotation a ship can possibly be in
            ###for each ship it check whether it has been found on the map, if not then it starts to correlate that ships pattern on all 'H' cells  
            for Rotation_Constant in range(4):
                if 'A' not in self.map:
                    Ship_rotation=numpy.rot90(AWing,Rotation_Constant)                                      #sets the ship patterns rotation
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Hit==True),Ship_rotation)        #finds all possible locations that the ship pattern can be in
                    Hit_Heat_Map+=Hit_Possible_Locations                                                    #combines the previous Heatmap with the new possible locations
                    
                if 'B' not in self.map:
                    Ship_rotation=numpy.rot90(BWing,Rotation_Constant)
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Hit==True),Ship_rotation)
                    Hit_Heat_Map+=Hit_Possible_Locations
                    
                    
                if 'Y' not in self.map:
                    Ship_rotation=numpy.rot90(YWing,Rotation_Constant)
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Hit==True),Ship_rotation)
                    Hit_Heat_Map+=Hit_Possible_Locations
                    
                    
                if 'X' not in self.map:
                    Ship_rotation=numpy.rot90(XWing,Rotation_Constant)
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Hit==True),Ship_rotation)
                    Hit_Heat_Map+=Hit_Possible_Locations
                
                
            Hit_Heat_Map=Hit_Heat_Map/Hit_Heat_Map.max()
  
            
            HMP_Flatten=Hit_Heat_Map.flatten()
            Sorted_Array=numpy.argsort(HMP_Flatten)[::-1]

            R,C = numpy.unravel_index(Sorted_Array,self.map.shape)

            Temp=[]
            for R,C in zip(R,C):
                if Hit_Heat_Map[R,C]>0:
                    if self.map[R,C]==' ':
                        Temp.append((R,C))
                
            if len(Temp) > 0:# if the Temp variable is above 0 then it output the value in Temp
                return Temp[0]
###################################################################################################################################################################################
###	If no guesses avaliable fall back to making a heat map of all the empty spaces avaliable
###	this program creates a heat map after a hit ship has been fully detected, this allows the part of
###	the program to so around the know ships which increases the accuracy of the next hit then compared to
###	to random guesses 																									

                
        elif 'H' not in self.map:
            ###The arrays below are the pattern for all the possible ships that the board can place
            ###These arrays will be used to determine all possible placements and orientations that they can be in to create a HeatMap
            #Y-wing pattern
            YWing=numpy.array([
                                                    [0,1,0],
                                                    [1,1,1],
                                                    [1,0,1]])
            #X-wing pattern
            XWing=numpy.array([
                                                    [0,1,0],
                                                    [1,1,1],
                                                    [0,0,0]])
            #B-wing pattern
            BWing=numpy.array([
                                                    [0,1,0],
                                                    [0,1,0],
                                                    [0,1,0]])
            #A-wing pattern
            AWing=numpy.array([
                                                    [0,1,1],
                                                    [0,1,0],
                                                    [0,0,0]])
            


            #Sets all the ship patterns into a single array so i can cycle through the array inside a loop
            XYBA=[YWing,XWing,BWing,AWing]
            #Stores and converts the map into the HitMap variable so i can use it later on in the program
            HitMap=numpy.array(self.map)


            #the Hit_Pattern variable is a array that will be used to find all Hit cells and set them to True
            Hit_Pattern=numpy.array([[False,False,False],
                                    [False,True,False],
                                    [False,False,False]])
            #Contain_Hit checks the HitMap array for any cells with a H (indicates a hit) and converts them to true
            Contains_Space = numpy.isin(HitMap,[' '])
#                 print(Contains_Hit)

            ###Below is a series of code that converts the map into a integer and also setting all letters into negative numbers
            m=numpy.array(self.map)
            m[m=='H']=10
            m[m==' ']=0
            m[m=='/']=1
            m[m=='X']=1
            m[m=='B']=1
            m[m=='Y']=1
            m[m=='A']=1
            m[m=='*']=1
            # converts the m array into a integer array
            m=m.astype(int)
            #sets all 1 inside the m array into  a negative number
            m[m=='1']=-1000
            #stores the m array into the Hit_Heat_Map array so i can be used to continuiously add numbers together in each cell later on in the code
            Hit_Heat_Map=m

            ###Below is the main program to create a Heat map for the map
            ###the for loop is needed to check all 4 directions of rotation a ship can possibly be in
            ###for each ship it check whether it has been found on the map, if not then it starts to correlate that ships pattern on all possible spots
            
            for Rotation_Constant in range(4):
                if 'A' not in self.map:
                    Ship_rotation=numpy.rot90(AWing,Rotation_Constant)                                          #sets the ship patterns rotation
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Space==True),Ship_rotation)          #finds all possible locations that the ship pattern can be in
                    Hit_Heat_Map+=Hit_Possible_Locations                                                        #combines the previous Heatmap with the new possible locations
                    
                if 'B' not in self.map:
                    Ship_rotation=numpy.rot90(BWing,Rotation_Constant)
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Space==True),Ship_rotation)
                    Hit_Heat_Map+=Hit_Possible_Locations
                    
                    
                if 'Y' not in self.map:
                    Ship_rotation=numpy.rot90(YWing,Rotation_Constant)
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Space==True),Ship_rotation)
                    Hit_Heat_Map+=Hit_Possible_Locations
                    
                    
                if 'X' not in self.map:
                    Ship_rotation=numpy.rot90(XWing,Rotation_Constant)
                    Hit_Possible_Locations=BattleShips.correlate((Contains_Space==True),Ship_rotation)
                    Hit_Heat_Map+=Hit_Possible_Locations


            Hit_Heat_Map=Hit_Heat_Map/Hit_Heat_Map.max()
 
            
            
            HMP_Flatten=Hit_Heat_Map.flatten()                                  #Flattens the Array into a 1d list
            Sorted_Array=numpy.argsort(HMP_Flatten)[::-1]                       #sorts the list from highest to lowest

            R,C = numpy.unravel_index(Sorted_Array,self.map.shape)              #unravels the list into rows and collums as if they were the original 2d array

            Temp=[]
            for R,C in zip(R,C):
                if Hit_Heat_Map[R,C]>0 and self.map[R,C]==' ' and (R+C)%2==0:   #a set of condititon a cell must follow inorder for it to be chosen next
                        Temp.append((R,C))
                
            if len(Temp) > 0:# if the Temp variable is above 0 then it output the value in Temp
                return Temp[0] 
