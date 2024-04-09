import random as rand
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def main():
    appendCheck = False
    newSet = False
    repo = 'none'
    road = 0
    aggressive = 0
    stopLights = -1
    data = []
    while True:
        startupChoice = input('Welcome to Traffic Genie!\n 1. Start Simulator\n 2. View Extra Functions\n 3. View data format\n')
        if startupChoice.lower() in ['1', '1.', 'start', 'start simulator', 'simulator']:
            choice = input('Would you like to use past data? (or start a new simulation) (Yes - Past data, No - new simulation)\n')
            while choice not in ['yes', 'Yes', 'No', 'no']:
                if choice in ['yes', 'Yes', 'No', 'no']:
                    break
                else:
                    print('Invalid input, please try again')
                    choice = input('Would you like to use past data or start a new simulation? (Yes - Past data, No - new simulation)\n')
            if choice in ['Yes', 'yes']:
                data = getPastData()
                if data == ['\nError, no past data! will create a new dataset\n']:
                    print(data[0])
                    dataFile = open('traffic_genie_data.txt', 'w')
                    newSet = True
                else:
                    dataFile = open('traffic_genie_data.txt', 'a')
                    appendCheck = True
            else:
                dataFile = open('traffic_genie_data.txt', 'w')
                newSet = True
            time = input('Enter time to be simulated over (minutes)\n')
            while int(time) < 1 or int(time) > 1440:
                print('Invalid input, please enter a number greater than or equal to one and less than or equal to 1440')
                time = input('Enter time to be simulated over (minutes)\n')
            time = int(time)
            newVehicle = True
            vehicles = []
            if appendCheck:
                repo = input('Would you like to enter additional data? (Yes, No)\n')
                while repo.lower() not in ['yes','no']:
                    print('Error, invalid choice! type Yes or No\n')
                    repo = input('Would you like to enter new data or use old data for simulation? (Yes --> new data, No --> use old data)\n')
            if repo.lower() == 'yes' or newSet:
                while newVehicle == True:
                    vehicles.append([getVehicle(), getAmount()])
                    vehicleChoice = input('Would you like to add another vehicle?\n')
                    if vehicleChoice not in ['Yes', 'yes']:
                        newVehicle = False
            road = input('How long is the road? (miles)\n')
            while not road.isnumeric() or not float(road) > 0:
                print('Invalid input, please enter a positive number\n')
                road = input('How long is the road? (miles)\n')
            road = float(road)
            aggressive = input('What aggressiveness setting would you like? (1-10)\n')
            while not aggressive.isnumeric() or not float(aggressive) <= 10 or not float(aggressive) > 0:
                print('Error invalid input! Please enter a positive number between 1 and 10.')
                aggressive = input('What aggressiveness setting would you like? (1-10)')
            stopLights = input('Please enter the amount of stop lights (if none type 0)\n')
            while not stopLights.isnumeric() or not float(stopLights) >= 0 or not float(stopLights) % 1 == 0:
                print('Error invalid input! Please enter a whole number greater than or equal to zero.')
                stopLights = input('Please enter the amount of stop lights (if none type 0)\n')
            stopLights = int(stopLights)
            aggressive = int(aggressive)
            dataFile.write(str(road) + ',' + str(aggressive) + ',' + str(stopLights) + "\n")
            for i in vehicles:
                for q in range(i[1]):
                    thisLine = ''
                    for z in range(len(i[0])):
                        try:
                            i[0][z] = float(i[0][z])
                            thisLine += str(i[0][z]) + ','
                        except:
                            thisLine += str(i[0][z]) + ','
                    dataFile.write(thisLine + '\n')
                    data.append(i[0])
            dataFile.write('-------\n')
            killdata = []
            for i in data:
                if len(str(i).split(',')) < 6 or i == '-------':
                    killdata.append(data.index(i))
            killdata = sorted(killdata)
            for i in killdata:
                data.pop(i)
            if road == 0:
                road = float(data[0][0])
            if aggressive == 0:
                aggressive = float(data[0][1])
            if stopLights == -1:
                stopLights = float(data[0][2])
            emissions = 0
            usedCapacity = 0
            speeds = []
            emissionsEfficiency = []
            for i in range(1,len(data)):
                thisV = data[i][1] * data[i][5]
                thisE = data[i][2]
                usedCapacity += thisV
                emissions += thisE
                speedRating = road / data[i][4]
                speeds.append(speedRating)
                emissionRating = road * thisE
                emissionRating = emissionRating / data[i][1]
                emissionsEfficiency.append(emissionRating)
            speeds = sorted(speeds)
            emissionsEfficiency = sorted(emissionsEfficiency)
            vehicles = len(data) - 1
            length = getLength(data)
            availableSpace = (road * 1609.34) / length
            speedLimit = 'no'
            limitChoice = input('Would you like to use a speed limit in the simulation? [mph] (type speed limit otherwise type no)\n')
            if limitChoice not in ['no','No','NO','nO'] and limitChoice.isnumeric():
                speedLimit = float(limitChoice)
            realSpeed = []
            perPassSpeed = []
            for i in range(1,len(data)):
                delta = rand.randint(0,aggressive)
                posmin = rand.randint(-1,1)
                if speedLimit != 'no':
                    if data[i][4] > speedLimit:
                        simSpeed = road / (speedLimit + (delta * posmin))
                    else:
                        simSpeed = road / (data[i][4] + (delta * posmin))
                else:
                    simSpeed = road / (data[i][4] + (delta * posmin))
                realSpeed.append(simSpeed)
                perPassSpeedHold = data[i][1] / simSpeed
                perPassSpeed.append(perPassSpeedHold)
            avgSimSpeed = sum(perPassSpeed) / len(perPassSpeed)
            avgEmission = sum(emissionsEfficiency) / len(emissionsEfficiency)
            carbon = avgEmission * road # in grams
            with PdfPages('Traffic_Charts.pdf') as pdf:
                # Create a new figure with two subplots (axes)
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
                # Call the modified functions with the axes as arguments
                summary_text = emissionFind(data, ax1)
                summary_text += efficiencyFind(data, time, road, ax2, aggressive)
                fig.text(0.05, 0.05, summary_text, fontsize=12, wrap=True, horizontalalignment='left', verticalalignment='bottom')
                # Save the figure with the pie charts to the PDF
                pdf.savefig(fig)
                # Close the figure
                plt.close(fig)
            break
        elif startupChoice.lower() in ['2', '2.', 'extra', 'view extra functions', 'functions', 'help']:
            print('\nExtra Functions of Traffic Genie\n')
            print('Using your own data\n')
            print('To use your own data, you can name your file "traffic_genie_data.txt"')
            print('Then use the data format of: \n\nlength of road,aggressiveness,stoplights\n --then enter as many vehicles as you like using this data format:\n vehicle type,passengers,CO2 emissions in g/mi,price ($),speed (mph),uses per day\n\n --Using this data format your file will be read into the simulator if you select the use past data option\n and your own data file is in the same file as the program.')
        elif startupChoice.lower() in ['3','3.','view data format', 'data format', 'data', 'format']:
            print('\nThe data format is:')
            print('length of road,aggressiveness,stoplights')
            print('--then use the next format for as many vehicles as you like with a new line being a new vehicle')
            print('vehicle type,passengers,CO2 emissions (g/mi),price ($),speed (mph),uses per day')

def getVehicle():
    type = input('Enter vehicle type (Car, Truck, Van, Motorcycle, Bus, Bike, other: specify other type)\n')
    smog = input('Enter the vehicles emissions of CO2 in grams per mile (g/mi)\n')
    if smog.isnumeric():
        smog = float(smog)
    else:
        while not smog.isnumeric():
            print('Invalid input, please enter a number\n')
            smog = input('Enter the vehicles emissions of CO2 in grams per mile (g/mi)\n')
    pph = input('How many people can fit in this vehicle?\n')
    if pph.isnumeric() and float(pph) % 1 == 0 and float(pph) > 0:
        pph = int(pph)
    else:
        while not (pph.isnumeric() and float(pph) % 1 == 0 and float(pph) > 0):
            print('Invalid input, please enter a positive whole number\n')
            pph = input('How many people can fit in this vehicle?\n')
    price = input('What is the cost of the vehicle?\n')
    if price.isnumeric() and float(price) > 0:
        price = float(price)
    else:
        while not (price.isnumeric() and float(price) > 0):
            print('Invalid input, please enter a positive number\n')
            price = input('What is the cost of the vehicle\n')
    speed = input('How fast can this vehicle go? (mph)\n')
    if speed.isnumeric() and float(speed) > 1000:
        print('Please enter a realistic number\n')
        while float(speed) > 1000:
            speed = input('How fast can this vehicle go?\n')
    if float(speed) < 0 or float(speed) > 1000:
        print('Please enter a realistic positive number\n')
    elif speed.isnumeric() and float(speed) > 0:
        speed = float(speed)
    else:
        while not (speed.isnumeric() and float(speed) > 0):
            print('Invalid input, please enter a positive number\n')
            speed = input('How fast can this vehicle go? (mph)\n')
    freq = input('How many times is this vehicle expected to be used per day?\n')
    if freq.isnumeric() and float(freq) > 0 and float(freq) % 1 == 0:
        freq = int(freq)
    else:
        while not (freq.isnumeric() and float(freq) > 0 and float(freq) % 1 == 0):
            print('Invalid input, please enter a positive whole number\n')
            freq = input('How many times is this vehicle expected to be used per day?\n')
    return ([type, pph, smog, price, speed, freq])

def getAmount():
    amount = input('How many of these vehicles?\n')
    while not amount.isnumeric() and not int(amount) > 0:
        print('Error invalid input! Please enter a positive whole number\n')
        amount = input('How many of these vehicles?\n')
    amount = int(amount)
    return(amount)

def fileCheck(filename):
    try:
        with open(filename, 'r'):
            return(True)
    except FileNotFoundError:
        return(False)

def getPastData():
    kill = []
    if fileCheck('traffic_genie_data.txt'):
        file = open('traffic_genie_data.txt', 'r')
        file = file.readlines()
        count = 0
        runner = []
        for i in range(len(file)):
            if file[i] == '-------':
                count += 1
            else:
                file[i] = file[i].split(',')
                for q in range(len(file[i])):
                    try:
                        file[i][q] = float(file[i][q])
                    except:
                        continue
            if i != 0 and file[i][0] != '-------\n' and len(file[i]) > 3:
                file[i].pop(file[i].index('\n'))
            elif (file[i][0] == '-------\n' or len(file[i]) < 4) and i != 0:
                kill.append(i)
        kill = sorted(kill, reverse=True)
        for i in kill:
            file.pop(i)
        return (file)
    else:
        return (['\nError, no past data! will create a new dataset\n'])

def getLength(data):
    length = 0
    for i in range(1, len(data)):
        if data[i][0].lower() == 'bike':
            length += 1.75
        elif data[i][0].lower() == 'car':
            length += 4.25
        elif data[i][0].lower() == 'truck':
            length += 6.02
        elif data[i][0].lower() == 'bus':
            length += 12.2
        elif data[i][0].lower() == 'van':
            length += 5.5
        elif data[i][0].lower() == 'motorcycle':
            length += 1.8
    return(length)

def emissionFind(dataList, ax):
    dataList.pop(0)
    names = []
    for i in dataList:
        if i[0].lower() not in names:
            names.append(i[0].lower())
    nameHold = []
    valuesDict = {}
    for i in names:
        valuesDict[i] = 0
    for q in dataList:
        if q[0].lower() == i:
            valuesDict[i] = valuesDict.get(i) + q[2]
    emissionsList = []
    for i in valuesDict.keys():
        emissionsList.append([i, valuesDict[i]])
    emissionsList = sorted(emissionsList, key = lambda x: x[1])
    emissionsList = [i for i in emissionsList if i[1] > 0]
    labels = [i[0] for i in emissionsList]
    values = [i[1] for i in emissionsList]
    ax.pie(values, labels = labels, autopct='%1.1f%%')
    ax.set_title('Emissions')
    totalEm = sum(values)
    for i in range(len(values)):
        if values[i] > (totalEm / 2):
            return(labels[i] + ' is emitting more than half your CO2, consider using more eco-friendly or efficient transportation.')
    return('The distribution of CO2 is sufficiently spread out, though you should always try to limit this as much as possible.')

def efficiencyFind(dataList, time, roadDistance, ax, agg):
    dataList.pop(0)
    names = []
    for i in dataList:
        if i[0].lower() not in names:
            names.append(i[0].lower())
    valuesDict = {}
    for i in names:
        valuesDict[i] = 0
    for q in dataList:
        if q[0].lower() == i:
            valuesDict[i] = valuesDict.get(i) + 1
    countList = []
    for i in valuesDict.keys():
        countList.append([i, valuesDict[i]])
    countList = sorted(countList, key = lambda x: x[1])
    speedsDict = {}
    for i in names:
        speedsDict[i] = 0
    for q in dataList:
        if q[0].lower() == i:
            valuesDict[i] = valuesDict.get(i) + q[4]
    for i in names:
        delta = rand.randint(0,agg)
        posmin = rand.randint(-1,1)
        speedsDict[i] = (speedsDict.get(i) / valuesDict.get(i)) + (delta * posmin)
    speedsList = []
    for i in speedsDict.keys():
        speedsList.append([i, speedsDict[i]])
    speedsList = sorted(countList, key = lambda x: x[1])
    available = []
    freqDict = {}
    for i in speedsList:
        a = roadDistance / i[1]
        a = a * 60
        b = a / time
        freqDict[i[0]] = b
    passengersDict = {}
    for i in names:
        passengersDict[i] = 0
    for q in dataList:
        if q[0].lower() == i:
            passengersDict[i] = passengersDict.get(i) + q[1]
    for i in names:
        passengersDict[i] = passengersDict.get(i) / valuesDict.get(i)
    effDict = {}
    for i in freqDict.keys():
        effDict[i] = freqDict.get(i) * passengersDict.get(i)
    values = list(effDict.values())
    labels = list(effDict.keys())
    ax.pie(values, labels = labels, autopct='%1.1f%%')
    ax.set_title('Efficiency (Speed and time only)')
    aq = '\n'
    for i in effDict.keys():
        aq += str(i) + ": " + str(round(effDict.get(i), 4)) + ' Efficiency Rating. \n'
    return(aq)

if __name__ == "__main__":
    main()
