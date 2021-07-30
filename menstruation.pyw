from datetime import datetime, timedelta
import tkinter
from tkinter import ttk, messagebox
from tkcalendar import Calendar

def main():
    global root
    root.geometry("297x292")
    
    Cal = Calendar(root, setmode="day", date_pattern="dd/mm/y", maxdate=datetime.now())
    Cal.place(x=23, y=35)

    def lastMenstruation_ovulation_fertility_nextMenstruation():

        root.geometry("1060x244")
        
        global last_menstruation
        last_menstruation = datetime.strptime(Cal.get_date(), "%d/%m/%Y")
        last_menstruation_formatted = last_menstruation.strftime("%B %#d, %#Y")
        last_menstruation_tx = tkinter.Label(root, text=f"Your last period started on {last_menstruation_formatted}", bg="white", font=("Segoe UI",16))
        last_menstruation_tx.place(x=280,y=35)
        
        cal_type_tx.config(text="Ovulation Date")
        
        # Find ovulation day
        ovulation_date = last_menstruation + timedelta(days=cycle - 14)
        ovulation_date_formatted = ovulation_date.strftime("%B %#d, %#Y")
        
        ovu_tx = tkinter.Label(
            root, text=f"You ovulate on {ovulation_date_formatted}", font=("Segoe UI",16), bg="white")
        ovu_tx.place(x=280,y=70)
        
        # Create Ovulation Calendar
        ovu_cal = Calendar(
        root, setmode="day", day=ovulation_date.day, month=ovulation_date.month, year=ovulation_date.year)
        ovu_cal.place(x=23,y=35)
        
        # Find your fertility days
        fertility_start = ovulation_date + timedelta(days=-3)
        fertility_start_formatted = fertility_start.strftime("%B %#d, %#Y")
        fertility_end = ovulation_date + timedelta(days=1)
        fertility_end_formatted = fertility_end.strftime("%B %#d, %#Y")
        
        fertility_tx = tkinter.Label(
            root, text=f"Your fertile window starts on {fertility_start_formatted} and ends on {fertility_end_formatted}"
            , font=("Segoe UI",16), bg="white")
        fertility_tx.place(x=280,y=105)

        # Find next menstruation
        next_menstruation = last_menstruation + timedelta(days=cycle)
        next_menstruation_formatted = next_menstruation.strftime("%B %#d, %#Y")

        next_menstruation_tx = tkinter.Label(
            root, text=f"Your next period will begin on {next_menstruation_formatted}"
            , font=("Segoe UI",16), bg="white")
        next_menstruation_tx.place(x=280,y=140)

        # Calculate another cycle
        def restart():
            root.destroy()
            ask_cycle()
        retry_bt = ttk.Button(text="Calculate another cycle", command=restart).place(x=280,y=185)

        #Navigate to next or previous cycle
        def refresh_tx():
            last_menstruation_formatted = last_menstruation.strftime("%B %#d, %#Y")
            if last_menstruation > datetime.now():
                last_menstruation_tx.config(text=f"Your period starts on {last_menstruation_formatted}")
            else:
                last_menstruation_tx.config(text=f"Your last period started on {last_menstruation_formatted}")
            ovulation_date = last_menstruation + timedelta(days=cycle - 14)
            ovulation_date_formatted = ovulation_date.strftime("%B %#d, %#Y")
            ovu_tx.config(text=f"You ovulate on {ovulation_date_formatted}")
            try:    
                ovu_cal.selection_set(ovulation_date)
            except ValueError:
                pass
            fertility_start = ovulation_date + timedelta(days=-3)
            fertility_start_formatted = fertility_start.strftime("%B %#d, %#Y")
            fertility_end = ovulation_date + timedelta(days=1)
            fertility_end_formatted = fertility_end.strftime("%B %#d, %#Y")
            fertility_tx.config(text=f"Your fertile window starts on {fertility_start_formatted} and ends on {fertility_end_formatted}")
            next_menstruation = last_menstruation + timedelta(days=cycle)
            next_menstruation_formatted = next_menstruation.strftime("%B %#d, %#Y")
            if next_menstruation < datetime.now():
                next_menstruation_tx.config(text=f"Your next period started on {next_menstruation_formatted}")
            else:
                next_menstruation_tx.config(text=f"Your next period will begin on {next_menstruation_formatted}")
        def previous():
            global last_menstruation
            try:
                last_menstruation += timedelta(days=-cycle)
            except OverflowError:
                return
            refresh_tx()
        def next():
            global last_menstruation
            try:
                last_menstruation + timedelta(days=cycle*2)
            except OverflowError:
                return
            last_menstruation += timedelta(days=cycle)
            refresh_tx()
        previous_bt = ttk.Button(text="< Previous", command=previous).place(x=418, y=185)
        next_bt = ttk.Button(text="Next >", command=next).place(x=493, y=185)

        # Remove unwanted tkinter objects
        Cal.destroy()
        last_menstruation_bt.pack_forget()
        
    
    last_menstruation_bt = ttk.Button(
        root, text="Select the start date of you last period", command=lastMenstruation_ovulation_fertility_nextMenstruation)
    last_menstruation_bt.pack(side="bottom", pady=23)

    cal_type_tx = tkinter.Label(root, text="Menstruation Date", font=("Segoe UI",14), bg="white")
    cal_type_tx.place(x=23,y=5,width=251)


def ask_cycle():
    global root
    root = tkinter.Tk()
    root.title("Menstruation+")
    root.geometry("400x100")
    root.config(bg="white")
    root.resizable(0,0)

    cycle_tx = tkinter.Label(text="How long is your menstrual cycle?", font=("Segoe UI",12), bg="white")
    cycle_tx.pack(pady=10)
    
    def arrow_clicked():
        cycle_menu.set("")

    #Everything related to the Comcobox
    selected_day = tkinter.StringVar()
    cycle_menu = ttk.Combobox(root, textvariable = selected_day, width=14, postcommand=arrow_clicked)
    cycle_menu['values'] = (21,22,23,24,25,26,27,28,29,30,31,32,33,34,35)
    cycle_menu.set("Number of days")
    cycle_menu.focus()
    cycle_menu.selection_range(0,14)
    cycle_menu.place(x=109, y=50, height=23)

    #Get the value entered in the Combobox and close the window
    def get_cycle():
        def Move_on():
            cycle_tx.destroy()
            cycle_menu.destroy()
            select_bt.destroy()
            main()
        
        global cycle
        cycle = cycle_menu.get()
        try:
            cycle = int(cycle)
        except ValueError:
            messagebox.showerror(title="Invalid Value", message="You may only enter numbers.")
            cycle_menu.focus()
            if cycle == "Number of days":
                cycle_menu.selection_range(0,14)
            else:
                cycle_menu.selection_clear()
        else:
            if cycle < 17 or cycle > 60:
                messagebox.showerror(title="Invalid Number", message="The number must be between 17 and 60 inclusive.")
                cycle_menu.focus()
            elif cycle < 20 or cycle > 40:
                ask_unusual_cycle = messagebox.askyesno(title="Unusual cycle", message="An average cycle is 20 to 40 days long. Are you sure you entered the correct information?")
                if ask_unusual_cycle == True:
                    Move_on()
                else:
                    return
            else:    
                Move_on()
    
    select_bt = ttk.Button(text="OK", command=get_cycle)
    select_bt.place(x=216, y=49)

    root.mainloop()

ask_cycle()