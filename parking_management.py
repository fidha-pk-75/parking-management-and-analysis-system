from datetime import datetime
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Vehicle:
    def __init__(self,veh_no,veh_type,owner_name):
        self.veh_no = veh_no
        self.veh_type = veh_type
        self.owner_name = owner_name
    def display_details (self):
        print("Vehicle Number:",self.veh_no)
        print("Vehicle Type:",self.veh_type)
        print("Owner Name:",self.owner_name,"\n")

class ParkingSlot:
    def __init__(self,slot_no,is_available,vehicle):
        self.slot_no = slot_no
        self.is_available = is_available
        self.vehicle = vehicle
    def display_slot_details(self):
        print("_______Slot Availability_____")
        print("Slot No : ",self.slot_no)
        print("Available : ",self.is_available)

        if self.vehicle is not None:
            self.vehicle.display_details()
        else:
            print("NO VEHICLE PARKED")
    def park_vehicle(self):
        if not self.is_available:
            print("Slot is already occupied")
            return
        
        vehicle_no = input("Enter vehicle NO :")
        if not vehicle_no:
                print("Enter Valid Vehicle no !!")
                return
        vehicle_type = input("Enter vehicle type : ")
        if not vehicle_type:
            print("!! Vehicle type Cannot be empty !!")
            return
        owner_name = input("Enter Owner Name : ")
        if not owner_name :
            print("!! Owner name cannot be empty !!")
            return

        vehicle = Vehicle(vehicle_no,vehicle_type,owner_name)
        self.vehicle = vehicle
        self.is_available = False
        print("Vehicle parked successfully")
    def remove_vehicle(self):
        if self.vehicle is not None:
            self.vehicle = None
            self.is_available = True
            print("Vehicle removed successfully")
        else:
            print("Slot is already empty")

class ParkingLot:
    def __init__(self,total_no_of_slots):
        self.total_no_of_slots = total_no_of_slots
        self.slots =[]
        self.ticket_counter = 1
        self.tickets = []

        for i in range(1,self.total_no_of_slots + 1):
            slot = ParkingSlot(i,True,None)
            self.slots.append(slot)
    def display_all_slots(self):
        print("DISPLAYING ALL SLOTS")
        for slot in self.slots:
            slot.display_slot_details()
    def park_vehicle(self):
        try:
            slot_no = int(input("Enter slot no: "))
        except ValueError:
            print("Enter a Valid number")
            return
        if slot_no < 1 or slot_no > self.total_no_of_slots:
            print("Invalid Slot no")
            return
            
        for i in self.slots:
            if i.slot_no == slot_no:
                if not i.is_available:
                    i.park_vehicle()
                    return
                i.park_vehicle()
                if i.vehicle is not None:
                    ticket = self.generate_ticket(i)
                    print("Ticket generated successfully")
                    print("Ticket ID:", ticket.ticket_id)
                return

        print("Invalid slot no")
    def remove_vehicle(self):
        try :
            slot_no = int(input("Enter slot no: "))
        except ValueError:
            print("! Please enter valid number !")
            return
        if slot_no < 1 or slot_no > self.total_no_of_slots:
            print("Invalid slot number")
            return
        for i in self.slots:
            if i.slot_no == slot_no:
                if i.vehicle is None:
                    print("Slot is already empty")
                    return
                for ticket in self.tickets:
                    if ticket.slot_no == i.slot_no and ticket.exit_time is None:
                        ticket.exit_time = datetime.now()
                        duration = ticket.calculate_duration()
                        fee = ticket.calculate_fee()
                        ticket.duration = duration
                        ticket.fee = fee

                        print("\n----- Parking Bill -----")
                        print("Ticket ID:", ticket.ticket_id)
                        print("Duration:", round(duration, 2), "hours")
                        print("Parking Fee: ₹", fee)
                        break
                i.remove_vehicle()
                return     
        print("Invalid slot no")
    def search_vehicle(self):
        veh_no = input("Enter vehicle no : ")
        if not veh_no:
            print("Vehicle number cannot be empty")
            return

        for i in self.slots:
            if i.vehicle is not None:
                if i.vehicle.veh_no == veh_no:
                    print("vehicle found in slot no : ",i.slot_no)
                    i.vehicle.display_details()
                    return
        print("vehicle not found")
    def display_available_slots(self):
        self.available_slots = []
        for i in self.slots:
            if i.is_available == True:
                self.available_slots.append(i.slot_no)
        if self.available_slots:
            print("Available slots are = ",self.available_slots)

        else:
            print("no slots available")
    def generate_ticket(self,slot):
        ticket_id = f'T{self.ticket_counter:03d}'
        ticket = ParkingTicket(ticket_id, slot.vehicle, slot.slot_no)
        self.tickets.append(ticket)
        self.ticket_counter += 1
        return ticket
    def display_ticket_history(self):
        if not self.tickets:
            print("No ticket history available")
            return

        for ticket in self.tickets:
            print("\nTicket ID:", ticket.ticket_id)
            print("Vehicle:", ticket.vehicle.veh_no)
            print("Slot:", ticket.slot_no)
            print("Entry:", ticket.entry_time)
            print("Exit:", ticket.exit_time)
            print("Duration:", round(ticket.duration, 2), "hours")
            print("Fee: ₹", ticket.fee)

    def numpy_analysis(self):
        fees = []

        for ticket in self.tickets:
            if ticket.exit_time is not None:
                fees.append(ticket.fee)

        arr = np.array(fees)

        if len(arr) == 0:
            print("No parking records")
            return

        print("Total Revenue:", np.sum(arr))
        print("Average Fee:", np.mean(arr))
        print("Maximum Fee:", np.max(arr))
        print("Minimum Fee:", np.min(arr))

    def pandas_analysis(self):
        data = []

        for ticket in self.tickets:
            if ticket.exit_time is not None:
                data.append([
                    ticket.ticket_id,
                    ticket.vehicle.veh_no,
                    ticket.vehicle.veh_type,
                    ticket.fee
                ])

        df = pd.DataFrame(
            data,
            columns=["Ticket ID", "Vehicle No", "Vehicle Type", "Fee"]
        )

        print(df)
        print("Total Records:", df.shape[0])
        print(df.head())
    def plot_chart(self):
        vehicle_types = []
        fees = []

        for ticket in self.tickets:
            if ticket.exit_time is not None:
                vehicle_types.append(ticket.vehicle.veh_type)
                fees.append(ticket.fee)

        if len(fees) == 0:
            print("No parking records")
            return

        plt.bar(vehicle_types, fees)
        plt.title("Parking Revenue")
        plt.xlabel("Vehicle Type")
        plt.ylabel("Parking Fee")
        plt.show()

class ParkingTicket:
    def __init__(self,ticket_id,vehicle,slot_no):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.slot_no = slot_no
        self.entry_time = datetime.now()
        self.exit_time = None
        self.duration = 0
        self.fee = 0

    def calculate_duration(self):
        if self.exit_time is None:
            self.exit_time = datetime.now()
        duration = self.exit_time - self.entry_time
        hours = duration.total_seconds() / 3600 
        return hours

    def calculate_fee(self):
        duration = self.calculate_duration()
        charged_hours = math.ceil(duration)
        parking_fee = charged_hours * 50
        return parking_fee
    
    

def main():
    parking = ParkingLot(5)

    while True:
        print("\n===== PARKING MANAGEMENT SYSTEM =====")
        print("1. Park Vehicle")
        print("2. Remove Vehicle")
        print("3. Search Vehicle")
        print("4. Display All Slots")
        print("5. Display Available Slots")
        print("6. Ticket History")
        print("7. NumPy Analysis")
        print("8. Pandas Analysis")
        print("9. Matplotlib Chart")
        print("0. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number")
            continue

        if choice == 1:
            parking.park_vehicle()
        elif choice == 2:
            parking.remove_vehicle()
        elif choice == 3:
            parking.search_vehicle()
        elif choice == 4:
            parking.display_all_slots()
        elif choice == 5:
            parking.display_available_slots()
        elif choice == 6:
            parking.display_ticket_history()
        elif choice == 7:
            parking.numpy_analysis()
        elif choice == 8:
            parking.pandas_analysis()
        elif choice == 9:
            parking.plot_chart()
        elif choice == 0:
            print("Thank you!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
