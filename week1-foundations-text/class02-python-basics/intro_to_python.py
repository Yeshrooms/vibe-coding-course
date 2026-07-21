#!/usr/bin/env python
# coding: utf-8

# # Intro to Python and Hello World Gemini!
# 
# - GSET Vibe Coding
# 
# 
# Niral Shah

# ## Some Python Fundamentals
# 
# Data Types - some key ones we'll be working with are Strings (text), Numbers (integers and decimals) and Booleans (true/false)
# 
# ### String (text)
# name = "Alex"
# favorite_color = "blue"
# 
# ### Numbers
# age = 16
# height = 5.8
# 
# ### Boolean (True/False)
# is_student = True
# 
# 

# In[ ]:


# Defining variables 

name = "Daniel"
age = 16
height = 5.8
is_student = True


# In[ ]:


# Printing output
favorite_color = input("What's your facvorite color?\n")
age = int(input("What's your age?\n"))


print(f"Hi, I'm {name}! I'm {age} years old and their favorite color is {favorite_color}")


# In[ ]:
if is_student:
    print(f'and {name} is a Student 🧑‍🎓')
else:
    print(f'and {name} is an adult 🤓')


# In[ ]:


# Asking for input

my_name = input("What's your name:\n")
print(f'Hi {my_name}!')



# ## Lists
# 
# Lists are collections of items that can hold multiple values. They're one of the most useful data structures in Python!

# In[ ]:


# Creating lists
fruits = ["apple", "banana", "orange", "grape"]
numbers = [1, 2, 3, 4, 5]
mixed_list = ["hello", 42, True, 3.14]

print("Fruits:", fruits)
print("Numbers:", numbers)
print("Mixed list:", mixed_list)


# In[ ]:


# Accessing items in lists (indexing starts at 0)
print("First fruit:", fruits[0])
print("Last fruit:", fruits[-1])

# Adding items to lists
fruits.append("strawberry")
print("After adding strawberry:", fruits)

# Length of a list
print("Number of fruits:", len(fruits))


# ## For Loops
# 
# For loops let us repeat actions for each item in a collection (like a list). They're perfect for processing multiple items!

# In[ ]:


# Basic for loop - going through each item in a list
print("All fruits:")
for fruit in fruits:
    print(f"- {fruit}")

print("\nSquaring numbers:")
for num in numbers:
    squared = num * num
    print(f"{num} squared is {squared}")


# In[ ]:


# Using range() to create a sequence of numbers
print("Counting from 1 to 5:")
for i in range(1, 6):
    print(f"Count: {i}")

print("\nCounting by 2s:")
for i in range(0, 11, 2):
    print(f"Even number: {i}")


# ## While Loops
# 
# While loops repeat actions as long as a condition is True. They're great when you don't know exactly how many times you need to loop!

# In[ ]:


# Basic while loop - countdown
countdown = 5
print("Countdown:")
while countdown > 0:
    print(f"{countdown}...")
    countdown -= 1  # Same as countdown = countdown - 1
print("Blast off! 🚀")


# In[ ]:


# While loop with user input (for demonstration)
# Note: This would wait for user input in an interactive environment
secret_number = 7
guess = 0

print("I'm thinking of a number between 1 and 10...")
while guess != secret_number:
    guess = int(input("What's your guess? "))
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print("You got it! 🎉")
        break

print("Done!")