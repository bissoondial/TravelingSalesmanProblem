#Avinash Bissoondial
#Traveling salesman problem, with greedy algorithm

#Importing needed libraries
import pandas as pd
import numpy as np
import mpu
import matplotlib.pyplot as plt
import random

#One of the parameters of this program was to make the randomness seeded. This command does that, seed can be changed, or removed for true randomness
# np.random.seed(123456)

#Importing the dataset of cities
Cities = pd.read_csv('uscities.csv')
Cities = Cities[['city', 'lat', 'lng']]

#Modularly defining different functions to make our program work:

#ChooseN(): simply allows the user to select a number of cities that will be traversed in the traveling salesman problem
def chooseN():
    try:
        nCities = int(input('How many cities do you want to visit?: '))
        print(f'{nCities} cities chosen')
        return(nCities)
    
    except:
        print('Invalid input. Please input an integer')

#CreateDistanceMatrix(): Calculates the distance between every combination of cities in the dataframe and inputs them into a pandas dataframe
def CreateDistanceMatrix(citiesVisited):
    n = len(citiesVisited)

    distanceMatrix = pd.DataFrame(index=citiesVisited['city'], columns=citiesVisited['city'])

    for i in range(n):
        for j in range(i, n):
            dist = mpu.haversine_distance((citiesVisited['lat'].iloc[i], citiesVisited['lng'].iloc[i] ), (citiesVisited['lat'].iloc[j], citiesVisited['lng'].iloc[j] ))

            #Filling the distanceMatrix
            distanceMatrix.iloc[i, j] = dist
            distanceMatrix.iloc[j, i] = dist
    
    return(distanceMatrix)

#FindClosestCity(): This will find and return the closest city that was not already 'visited' / present in the list 'path'
def FindClosestCity(row, path):
    filtered_row = [row[i] for i in range(len(row)) if i not in path]

    if not filtered_row:
        return None
    
    return min(filtered_row)

#GetTotalDistance(): This just computes the total distance of a tour given a list of indexes
def GetTotalDistance(path, distanceMatrix):
    total_distance = 0

    for i in range(len(path) - 1):
        row1 = path[i]
        column1 = path[i + 1]

        total_distance += distanceMatrix.iloc[row1, column1]

    return(total_distance)

#NextAlgorithm(): Simply asks the user if they want to use the next random hill algorithm to optimize the solution
def NextAlgorithm():
    YorN = input('Would you like to test another algorithm? Input Y or N: ')

    if YorN == 'Y':
        print('Next algorithm loading...')
        return 1
    elif YorN =='N':
        print('Ok. Program ended.')
        return 0
    else: 
        print('Invalid input')
        NextAlgorithm()

#RandomHillLocalSearch(): This is a simple hill climbing algorithm, will randomly change something and see if the distance is lower. Will continue until the limit
#input by the user is reached. One of the drawbacks to this simple algorithm is that the user can get stuck in a local minima. 
def RandomHillLocalSearch(path, distanceMatrix):
    limit = int(input('How many times do you want to try the new algorithm? (the limit): '))
    distance = GetTotalDistance(path, distanceMatrix)
    counter = 0
    newpath = path.copy()
    winningpath = None

    while counter < limit:
        i1, i2 = random.sample(path[1:-1], 2)
        newpath[i1], newpath[i2] = newpath[i2], newpath[i1]
        newdistance = GetTotalDistance(newpath, distanceMatrix)
        if newdistance < distance:
            winningpath = newpath.copy()
            distance = newdistance
        else: 
            newpath = path.copy()
        
        counter += 1

    if winningpath == None:
        return None
    else: 
        return winningpath





#Actual program:

#Choose number of cities
nCities = chooseN()
#Randomly sample that number of cities
citiesVisited = Cities.sample(n=nCities, replace=False)
#Create a distance matrix with those cities 
distanceMatrix = CreateDistanceMatrix(citiesVisited)
#Defining the list 'path' and index of current city
path = [0]
currentcity = 0
#This is the greedy algorithm: grab the row of the current city output the closest city that was not already visited
while len(path) < nCities:
    rowlist = distanceMatrix.iloc[currentcity].tolist()

    currentcity = rowlist.index(FindClosestCity(rowlist, path))

    if currentcity != None:
        path.append(currentcity)

path.append(0)

#Converting the list of city indexes to the city names:
path_citynames = []
for i in path:
    path_citynames.append(citiesVisited['city'].iloc[i])

#Finding the total distance of the tour:
total_distance = GetTotalDistance(path, distanceMatrix)

#Outputting the results:
print(f'The tour of the chosen cities is the following: {path_citynames}\n The total distance traveled is {total_distance} km')
print('A graph of the tour is being generated...')

#Outputting a graph of the tour
indexes = list(range(nCities))
indexes.append(0)

Xcoors = citiesVisited.iloc[path]['lat']
Ycoors = citiesVisited.iloc[path]['lng']

try: 
    plt.style.use('Solarize_Light2')
except: 
    plt.figure(facecolor='lightblue')

plt.plot(Xcoors, Ycoors, marker='o')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('City Tour using Greedy Algorithm')

for i, index in enumerate(indexes):
    plt.text(Xcoors.iloc[i], Ycoors.iloc[i], str(index), fontsize=15, ha='right', va='bottom')

plt.grid(True, alpha=0.5, linestyle='--')
plt.show()

#Using another algorithm to optimize the tour if the user selects to

next = NextAlgorithm()
if next == 1:
    newpath = RandomHillLocalSearch(path, distanceMatrix)
else: 
    newpath = 0

#Random hill algorithm will output 'None' if there is no better path found
if newpath == 0:
    pass
elif newpath == None:
    print('No better path was found. Ending program.')
else: 
    optimizeddistance = GetTotalDistance(newpath, distanceMatrix)
    #Converting our newpath into city names to be printed:
    newpath_citynames = []
    for i in newpath:
        newpath_citynames.append(citiesVisited['city'].iloc[i])
    #Outputting our new tour:
    print(f'A new more optimal path was found! The tour will now travel a total distance of {optimizeddistance}!\n The new tour is the following order: {newpath_citynames}')
    print('Generating a new graph and ending program.')

    indexes = list(range(nCities))
    indexes.append(0)

    Xcoors = citiesVisited.iloc[newpath]['lat']
    Ycoors = citiesVisited.iloc[newpath]['lng']

    try: 
        plt.style.use('Solarize_Light2')
    except: 
        plt.figure(facecolor='lightblue')

    plt.plot(Xcoors, Ycoors, marker='o')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('City Tour using Random Hill Local Search Algorithm')

    for i, index in enumerate(indexes):
        plt.text(Xcoors.iloc[i], Ycoors.iloc[i], str(index), fontsize=15, ha='right', va='bottom')

    plt.grid(True, alpha=0.5, linestyle='--')
    plt.show()

    