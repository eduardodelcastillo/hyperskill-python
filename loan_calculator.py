import math, argparse, sys

month = year = period = 0.0

def calc_annuity_payment(counter):
    payment = loan_principal * (nominal_interest * (1 + nominal_interest) 
                        ** number_of_periods) / ((1 + nominal_interest)
                        ** number_of_periods - 1)
    return int(math.ceil(payment))

def calc_diff_payment(counter):
    m = counter
    payment = loan_principal / number_of_periods + nominal_interest * (loan_principal - (loan_principal * (m - 1) / number_of_periods))
    return int(math.ceil(payment))

parser = argparse.ArgumentParser(description="This app calculates Annuity or Differentiated payments.")

parser.add_argument("--type", choices=["annuity", "diff"], 
                    help="Please choose Annuity or Differentiated type of calculation")
parser.add_argument("--principal", type=float,
                    help="Please enter the principal loan amount")
parser.add_argument("--interest", type=float,
                    help="Please enter the annual interest")
parser.add_argument("--periods", type=int,
                    help="Please enter the number of months needed to pay the loan")
parser.add_argument("--payment", type=int,
                    help="Please enter the payment amount per month")

args = parser.parse_args()
value_list = []

for arg in vars(args):
    if getattr(args,arg) is not None:
        value_list.append(getattr(args,arg))

#Check for proper arguments:
if len(sys.argv) < 3:
    print("Incorrect parameters")
    sys.exit()
elif args.type == None:
    print("Incorrect parameters")
    sys.exit()

calculation_type = args.type
loan_principal = args.principal
number_of_periods = args.periods
interest = args.interest
month_payment = args.payment

#print(value_list)
#check if input value is negative:
for counter in value_list[1:]:#skips first item in value_list
    if counter < 0:
        print("Incorrect parameters")
        sys.exit()
    counter += 1

if calculation_type == "annuity":
    total_payment = 0
    #check for the 3 parameters
    #Calculate periods:
    if loan_principal is not None and month_payment is not None and interest is not None and number_of_periods is None:
        nominal_interest = interest / (12 * 100)
        period = math.log(month_payment/(month_payment - nominal_interest * loan_principal), 1 + nominal_interest)
        # Decoding number of years and months
        year = math.floor(period / 12)
        month = math.ceil(period % 12)
        if month == 12:
            year += 1
            month -= 12

        if year == 1:
            if month == 1:
                print(f"It will take {year} year and {month} month to repay this loan!")
            elif month == 0:
                print(f"It will take {year} year to repay this loan!")
            else:
                print(f"It will take {year} year and {month} months to repay this loan!")
        elif year == 0:
            if month == 1:
                print(f"It will take {month} month to repay this loan!")
            else:
                print(f"It will take {month} months to repay this loan!")   
        elif month == 0:
            print(f"It will take {year} years to repay this loan!")                
        else:
            print(f"It will take {year} years and {month} months to repay this loan!")
        
        #Calculate overpayment
        for counter in range(1, math.ceil(period) + 1):
            total_payment += month_payment
         
        overpayment = int(total_payment - loan_principal)
        print(f"Overpayment = {overpayment}")       
    #calculate annuity
    elif loan_principal is not None and interest is not None and number_of_periods is not None and month_payment is None:
        nominal_interest = interest / (12 * 100)
        for counter in range(1, number_of_periods + 1):
            annuity_payment = calc_annuity_payment(counter)
            total_payment += annuity_payment
        #calculate overpayment:
        overpayment = int(total_payment - loan_principal)    
        print(f"Your annuity payment = {annuity_payment}!")
        print(f"Overpayment = {overpayment}")
    #Calculate principal:
    elif month_payment is not None and interest is not None and number_of_periods is not None and loan_principal is None:
        nominal_interest = interest / (12 * 100)
        loan_principal = round(month_payment / ((nominal_interest * (1 + nominal_interest) 
                                       ** number_of_periods) / (((1 + nominal_interest)
                                       ** number_of_periods) - 1)))
        print(f"Your loan principal = {loan_principal}!")
        #Calculate overpayment
        for counter in range(1,number_of_periods + 1):
            total_payment += month_payment
        overpayment = int(total_payment - loan_principal)
        print(f"Overpayment = {overpayment}")
    elif interest is None:
        print("Incorrect parameters")
        sys.exit()        
elif calculation_type == "diff":
    #Check if it has all required arguments: principal, interest, periods
    if loan_principal is not None and interest is not None and number_of_periods is not None:
        nominal_interest = interest / (12 * 100)
        counter = 0
        total_payment = 0
        for counter in range(1, number_of_periods + 1):
            month_payment = calc_diff_payment(counter)
            print(f"Month {counter}: payment is {month_payment}")
            total_payment += month_payment
        
        #calculate overpayment:
        overpayment = int(total_payment - loan_principal)
        print(f"\nOverpayment = {overpayment}")
    else:
        print("Incorrect parameters")
        sys.exit()
else:
    print("Incorrect parameters - last else")
    sys.exit()