import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
import string
from string import digits
from string import punctuation

customer_detail=[]
rented_car=[]

def menu():     # INFORMATION ABOUT THE CHOICES USER CAN MAKE
    print("You may select one of the following:\n1) List available cars\n2)Rent a car\n3)Return a car\n4)Count the money\n0)Exit")
    return int(input("What is your selection?\n"))

def manual_join(items, delimiter=","):
    #Joins a list of strings using a delimiter.
    result = ""
    for i in range(len(items)):
        result += items[i]
        if i < len(items) - 1:
            result += delimiter
    return result

def manual_join1(items, delimiter=", "):
    #Joins a list of strings using a delimiter and a space.
    result = ""
    for i in range(len(items)):
        result += items[i]
        if i < len(items) - 1:
            result += delimiter
    return result


def available_vehicle():        #INFORMATION ABOUT THE AVAILABLE VEHICLES IN THE COMPANY
    f= open("vehicles.txt","r")
    g=open("rentedVehicles.txt","r")
    data_1=f.readlines()
    data_2=g.read()
    cars=[]
    rented=[]
    available_cars=[]
    for items in data_1:
        cars.append(items.strip().split(","))
    for item in data_2:
        rented.append(item.strip().split(","))
    for car in cars:
        if car[0]  in data_2:
            cars.remove(car)
    i=0
    while i<len(cars):
        print(f"* Reg. nr: {cars[i][0]}, Model: {cars[i][1]}, Price per day: {cars[i][2]}\nProperties: {manual_join1(cars[i][3:])}")
        i+=1
    print()
    f.close()
    g.close()

def Rented_detail():            #FUNCTION TO APPEND THE NEW RENTED CAR INFORMATION
    f=open('rentedVehicles.txt','a+')
    f.write(manual_join(rented_car[:3])+"\n")
    f.close()

def email_address():            #VALIDATION OF EMAIL ADDRESS
    while True:
        email=input("Give your email:\n")
        e=email.split("@")
        if "@" in email and "." in e[-1]:
            customer_detail.insert(3,email)
            print("Hello",customer_detail[1])
            print("You rented the car",rented_car[0]+"\n")
            rented_car.insert(2,datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M"))
            customers_file()
            Rented_detail()
            break
        else:
            print("Give a valid email address.")
            continue

def customers_file():          # FUNCTION TO APPEND CUSTOMER DETAILS IN FILE
    f=open('customers.txt','a+')
    f.write(manual_join(customer_detail[:4])+"\n")
    f.close()

def returning_customer(data,birth_time):      #TO IDENTIFY THE RETURNING CUSTOMER
    details=[]
    for line in data:
        details.append(line.strip().split(","))
        
    for items in details:
        if birth_time in items:
            rented_cars=rented_car[:1]
            rented_cars.insert(1,birth_time)
            rented_cars.insert(2,datetime.strftime(datetime.now(),"%d/%m/%Y %H:%M"))
            f=open('rentedVehicles.txt','a+')
            f.write(manual_join(rented_cars)+"\n")
            f.close()
            print("Hello",items[1])
            print("You rented the car",rented_cars[0])
            break

def name():            # VALIDATION OF USER'S NAME
    while True:
        print("Names contain only letters and start with capital letter.")
        first_name=input("Enter the first name of the customer:\n")
        second_name=input("Enter the second name of the customer:\n")
        full_name= first_name+second_name
        if first_name[0].isupper() and first_name[1:].islower() and second_name[0].isupper() and second_name[1:].islower():
            for char in full_name:
                if char in digits or char in punctuation:
                    break
            else:
                customer_detail.insert(1,first_name)
                customer_detail.insert(2,second_name)
                email_address()        #CALLING EMAIL ADDRESS FUNCTION
                break
            
        else:
            continue
def return_car():         #FUNCTION TO RETURN THE RENTED CAR AND CALCULATE THE RENTED AMOUNT
    f=open("vehicles.txt","r")          #OPENING FILES IN READ MODE TO SEE DETAILS OF RENTED CAR 
    g=open("rentedVehicles.txt","r")
    car_no=input("Give the register number of the car you want to return:\n")
    data_1=f.readlines()
    vehicles_cost=[]
    rented_vehicles=[]
    transactions=[]
    data_2=g.readlines()
    for line in data_2:
        rented_vehicles.append(line.strip().split(","))

    for cars in data_1:
        vehicles_cost.append(cars.strip().split(","))

    for vehicles in vehicles_cost:
        if car_no in vehicles:
            for items in rented_vehicles:
                if car_no in items:
                     rented_date=datetime.strptime(items[2],"%d/%m/%Y %H:%M")
                     returning_date=datetime.now()
                     returning_date_str=datetime.strftime(returning_date,"%d/%m/%Y %H:%M")
                     no_of_days=(returning_date-rented_date).days
                     price_per_day=float(vehicles[2])
                     total_cost=(no_of_days*price_per_day)
                     total_cost_decimal=f"{total_cost:.2f}"
                     print(f"The rent lasted {no_of_days} days and the cost is {total_cost_decimal} euros\n")
                     transactions.append([car_no,items[1],items[2],returning_date_str,str(no_of_days),str(total_cost_decimal)])
                     rented_vehicles.remove(items)
                     break
            else:
                print("Car is not rented.\n")
                break
            break

    else:
        print("Car does not exist.\n")
        

    f.close()                                   #CLOSING THE FILES
    g.close()

    g=open("rentedVehicles.txt","w")            #OPENING FILE IN WRITE MODE TO CHANGE THE DATA IN FILE AFTER RETURNING THE RENTED CAR
    for items in rented_vehicles:
        new_data=manual_join(items)
        g.write(new_data+"\n")
    t=open("transActions.txt","a+")              #OPENING THE TRANSACTIONS IN WRITE MODE FILE TO ADD NEW TRANSACTIONS
    for lists in transactions:
        t.write(manual_join(lists)+"\n")
    g.close()                                   #CLOSING THE FILES
    t.close()
    
def birth():                                    # VALIDATION OF AGE OF USER
    while True:
        try:
            f=open("customers.txt","r")         #ACCESSING FILE THAT CONTAINS CUSTOMERS DETAILS
            data=f.readlines()
            t=input("Please enter your birthday in the form 'DD/MM/YYYY':\n")
            DOB=datetime.strptime(t,'%d/%m/%Y').date()
            today=date.today()
            age_in_days=(today-DOB).days
            age=int(age_in_days // 365)
            if age<18:
                print("You are too young to rent a car, sorry!\n")
                break
            elif age>=75:
                print("You are too old to rent a car, sorry!\n")
                break
            else:
                print("Age is Okay.")
                if t in (manual_join(data)):
                    returning_customer(data,t)      #CALLING RETURNING CUSTOMER FUNCTION
                    break
                else:
                    customer_detail.insert(0,t)
                    rented_car.insert(1,t)
                    name()    #CALLING NAME FUNCTION
                    f.close()       
                    break
            
        except ValueError:
            print("There is not such date. Try again!")
            continue
    

def renting_car():                          #FUNCTION FOR RENTING NEW CAR THAT HELPS TO IDENTIFY CARS AVAILABLE AND ALREADY RENTED CARS
    car_no=input("Give the register number of the car you want to rent:\n")
    f=open("vehicles.txt","r")              #OPENING AVAILABLE VEHICLES AND RENTED VEHICLES FILE IN READING MODE
    g=open("rentedVehicles.txt","r")
    data1 =f.readlines()
    data2=g.readlines()
    car_list=[]
    rented_car_list=[]
    for line in data2:
        b=line.strip().split(",")
        rented_car_list.append(b)
        
    for line in data1:
        a=line.strip().split(",")
        car_list.append(a)
        
    for rented in rented_car_list:
        if car_no in rented:
            print(car_no,"already rented.\n")
            break
   
    else:
        for item in car_list:
            if(car_no in item):
                print("Car is available")
                rented_car.insert(0,car_no)
                birth()
                break
            
        else:
            print("Car does not exist.\n")
        
    f.close()                               #CLOSING THE FILES
    g.close()

def count_money():  # TO CALCULATE TOTAL AMOUNT OF MONEY
    f=open("transActions.txt","r") #OPENING THE TRANSACTIONS FILE
    data=f.readlines()
    money=[]
    for items in data:
        money.append(items.strip().split(",")[5])
    total_income=0
    i=0
    while i < len(money):
        total_income += float(money[i])
        i+=1
        
    print(f"The total amount of money is {total_income:.2f} euros\n")
    f.close()   # CLOSING THE FILE
    
def main(): #PROVIDE THE INFORMATIONS FOR EACH CHOICES
    while True:
        try:
            choice=menu()
            if choice==1:
                print("The following cars are available:")
                available_vehicle() #CALLING FUNCTION TO THAT DISPLAYS LISTS OF CARS IN COMPANY
            elif choice==2:
                renting_car()       #CALLING FUNCTION TO RENT A CAR
            elif choice==3:
                return_car()        #CALLING FUNCTION TO RETURN THE RENTED CAR
            elif choice==4:
                count_money()       #CALLING FUNCTION TO CALCULATE THE TOTAL AMOUNT OF INCOME
            elif choice==0:
                print("Bye!")       #EXITING THE PROGRAM
                break
            else:
                print()
        except ValueError:          #CHECKS ANY VALUE ERRORS IN THE FUNCTION
            print()
            continue

main()                              #CALLING THE MAIN FUNCTION THAT CONTAINS OVERALL PROGRAM
