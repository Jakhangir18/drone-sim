altitudes = [12.5, 18.0 , 22.3 , 9.8, 25.0]

def average(numbers):
    return sum (numbers)/len (numbers)

def highest(numbers):
    top = numbers [0]
    for n in numbers:
        if n > top:
            top = n
    return top

print (f"readings:{altitudes}")
print (f"average: {average(altitudes)}")
print (f"highest: {highest(altitudes)}")

for a in altitudes:
    if a > 20:
        print(f"{a} m - high altitude warning")