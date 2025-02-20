#!/usr/bin/env python
# coding: utf-8

# HOW LONG TO MAKE $1,000,000
# 
#         run bottom cell or funtion "live()" to start program

# In[13]:


import time


# In[14]:


def get_age():
    age = int(input("How old are you? -- "))
    return age


# In[15]:


def ihave_bills():
    bills = 0
    ans = input("Do you want to calcuate expenses? y/n -- ")
    if ans == 'y':
        auto = int(input('How much is you car note? -- '))
        phone =int(input('How much is your phone bill? -- '))
        rent = int(input('How much is your rent? -- '))
        groc = int(input('What is your average monthly grocery cost? -- '))
        fuel = int(input('What is your average monthly fuel cost? -- '))
        misc = int(input('What is your average money waste? -- '))
        bills = auto + phone + rent + groc + fuel + misc
    else:
        bills = 0
        
    expenses = bills
    return expenses
        
        
    


# In[16]:


def start():
  
    print('************************************************************')
    print('************************************************************')
    print(' !!! ROAD TO $1,000,000 CASH !!! ')
    print('************************************************************')
    print("This is a small utility tool created by Joshua McMahon aka 'The 6th Dimension'. \n It's purpose is to give the user a very rough estimate of how long it would take them to accrue $1,000,000 right now with their current employer. \n It is meant to show my peers and those alike how important it is to give their creativty a change and to go chase their dreams.\n The life of our dreams is not possible through traditional employment alone. We must take risk, and be innovative. \n So to you... Take this info, put into perspective the changes you wish to make and go manifest your desires! \n With love, \n           --SIX")

    print('************************************************************')
    print('Instructions: Use integers(whole numbers only)')
    print('************************************************************')
    return


# In[17]:


def get_job_info():
    wage = int(input('What is your rate? -- '))
    clock = int(input('How many hours a day do you work? -- '))
    return  wage, clock


# In[18]:


def calculate_finance(wage, clock, bills):
    weekly = wage * clock * 5
    monthly = (weekly * 4)- bills
    yearly = monthly * 12
    return yearly
    


# In[19]:


def calulate_freedom(age,yearly):
    count = 0
    gross=0
    while gross < 1000000:
        age = age + 1
        gross = gross + yearly
        count = count + 1 
        print( f'At {age} years old')
        print(f'you will have collected ${gross} dollars. \n')
    return count


# In[23]:


def pause():
    time.sleep(3)
    
    print('\n \n Would you like to try again? y/n/q ("q" for quit, press "n to keep window open") --')
    response = input()
    
    
    if response == 'y': 
        live()
    elif response == 'n':
        print('May God grant you prosperity and good health.')
        time.sleep(20)
        
    elif response == 'q':
        print('.')
    else:
        print('.')
        
    
    


# In[24]:


def live():
    start()
    age  = get_age()
    wage, clock = get_job_info()
    expenses = ihave_bills()
    yearly = calculate_finance(wage,clock, expenses)
    calulate_freedom(age, yearly)
    
    print(' \n\n I encourage you to test the numbers for your dream job and other roles you may be seeking. \n Do everything you can to close the gap! Good luck, see you at $1,000,000! \n Check me out: www.github.com/the6thdimension , www.instagram.com/the6thdimension')
    
    
    pause()


# In[26]:


live()


# In[ ]:





# In[ ]:




