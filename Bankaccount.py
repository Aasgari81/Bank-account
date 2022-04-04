from decimal import Decimal as Dc
from datetime import datetime, timedelta
import unittest
def account_number_checker() -> "function":
    account_number_collection = []

    def account_number_inserter(acccount_nubmer : int)  :
        nonlocal account_number_collection
        if acccount_nubmer in account_number_collection : 
            raise ValueError("This number alredy Exist")
        else:
            account_number_collection.append(acccount_nubmer)
        return 
    return account_number_inserter

def transaction_id (starting_number : int):
    Transaction_id = starting_number - 1
    def id_producer ():
        nonlocal Transaction_id
        Transaction_id += 1
        return Transaction_id
    return id_producer

class timezone:
    def __init__ (self, city_name, offset_hour, offset_minute):
        if not isinstance(city_name, str):
            raise TypeError("City name should be string")
        if len(city_name.strip()) == 0 :
            raise ValueError("City name can't be empty")
        if offset_minute < -59 or offset_minute > 59 :
            raise ValueError("Offset minute should be between -59,+59")
        if not isinstance(offset_minute, int):
            raise TypeError("Offset minute should be integer")
        if not isinstance(offset_hour, int):
            raise TypeError("Offset hour should be integer")
        self.city_name = city_name
        offset = timedelta(hours = offset_hour, minutes = offset_minute)
        if offset < timedelta(hours = -12) or offset > timedelta(hours = +14):
            raise ValueError("Offset must be between -12:00 and +14:00")
        self.offset = offset
        self.offset_hours = offset_hour
        self.offset_minute = offset_minute

class Bankaccount:
    account_number_inserter = account_number_checker()
    interest_rate = Dc("0.5")
    def __init__ (self, account_number, city_name, first_name, last_name, time_zone_offset_hour, time_zone_offset_minute, balance):
        Bankaccount.account_number_inserter(account_number)
        if not isinstance(first_name, str):
            raise TypeError("First name should be string")

        if not isinstance(last_name, str):
            raise TypeError("Last name should be string")
        
        if not isinstance(balance, Dc):
            raise TypeError("Balance type should be decimal")
        
        if balance < 0:
            raise ValueError("Balance can't be negative")
        
        if len(city_name.strip()) == 0:
            raise ValueError("City name can't be empty")

        if len(first_name.strip()) == 0:
            raise ValueError("First name can't be empty")
        if len(last_name.strip()) == 0:
            raise ValueError("Last name can't be empty")
        Timezone = timezone(city_name, time_zone_offset_hour, time_zone_offset_minute)
        
        self.TImezone = Timezone
        self.account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        self.time_zone_offset_hour = time_zone_offset_hour
        self.time_zone_offset_minute = time_zone_offset_minute
        self._balance = balance
        self._fullname = f'{first_name} {last_name}'
        self.city_name = city_name
    
    def set_balance (self, value) : 
        if value < 0 :
            raise ValueError("Balance can't negative")
        self._balance = value
    def get_balance (self) : 
        print(self._balance)
    
    def get_fullname(self):
        print(self._fullname)
    
    def set_fullname(self, value):
        if not isinstance(value, str):
            raise ValueError("Full name should be integer")
        self._fullname = value
        return

    balance = property(fget = get_balance, fset = set_balance)
    fullname = property(fget = get_fullname, fset = set_fullname)
    Transaction_id = transaction_id(1)

    def confermation_generator(self, transaction_type):
        transaction_codes = {
        'deposit' : 'D',
        'withdraw' : 'W',
        'interest' : 'I',
        'rejected' : 'X'
        }
        transaction_ID = transaction_id()
        transaction_time = (datetime.utcnow()+self.timezone.offset).strftime('%Y%m%d%H%M%S')
        return f'{transaction_codes[transaction_type]}-{self.account_number}-{transaction_time}-{transaction_ID}'

    def withdrawal (self, amount):
        if not isinstance(amount, Dc):
            raise TypeError ("type of amount of money is decimal")
        if self.balance - amount < Dc("0.0"):
            print(Bankaccount.confermation_generator('rejected'))
            raise ValueError ("NOT enough balance")
        else:
            self.balance -= amount
            return Bankaccount.confermation_generator('withdraw')
    def deposit (self, amount):
        if not isinstance(amount, Dc):
            raise TypeError ("type of amount of money is decimal")
        self.balance += amount
        return Bankaccount.confermation_generator('deposit')
    
    def pay_interest(self):
        interest = self.balance * Bankaccount.interest_rate
        self.balance += interest
        return Bankaccount.confermation_generator('interest')

class confirmation_code_parser:

    def __init__ (self, confirmation_code):
        transaction_type, account_number, transaction_time, transaction_id = confirmation_code.split(sep = "-")
        self.transaction_type = transaction_type
        self.account_number = account_number
        self.transaction_time  = transaction_time
        self.transaction_id = transaction_id

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class test_classes(unittest.TestCase):

    def creating_timezone1 (self):
        tz1 =  timezone("tehran", 2, -30)
        self.assertequal("tehran", tz1.city_name)
        self.assretequal(timedelta(hours = 2, minutes = -30), tz1.offset)
        
    
    def creating_timezone2 (self):
        tz2 = timezone("tabriz", -2, -36)
        self.assertequal("tabriz", tz2.city_name)
        self.assertequal(timedelta(hours = -2, minutes = -36), tz2.offset_hours)
    
    def creating_timezone3 (self):
        with self.assertRaises(ValueError):
            tz3 = timezone("tehran", 12, 95)
    

    def creating_timezone4 (self):
        with self.assertRaises(ValueError):
            tz4 = timezone("tehran", 18, 95)
        
    def creating_account1 (self):
        account_number = 2325
        account_city = 'tehran'
        first_name = 'Ali'
        last_name = 'Asgari'
        offcet_hour= 3
        offset_min = 30
        balance = Dc("360")


        account = Bankaccount(account_number,account_city, first_name, last_name, offcet_hour, offset_min, balance)
        self.assertequal(account_number, account.account_number)
        self.assertequal(account_city, account.TImezone.city_name)
        self.assertequal(first_name, account.first_name)

    def creating_account2 (self):
        with self.assertRaises(TypeError):
            account = Bankaccount(2124, "mashhad", "ahmad", "mohamadi", 5, 54, 25.32)
        
    def creating_account3 (self):
        with self.assertRaises(ValueError):
            account = Bankaccount(2124, "hamedan", "akbar", "bagheri", 12, 24, Dc("515.22"))
            account1= Bankaccount(2124, "tehran", "mahdi", "hosseini", 11, 45, Dc("16516"))
    def creating_account (self):
        with self.assertRaises(ValueError):
            account = Bankaccount(2265, "kashan", "lamn", "knkn", 12, 21, Dc("-59"))
    
run_tests(test_classes)

