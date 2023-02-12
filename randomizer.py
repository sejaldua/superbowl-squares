import random
import time
import sys

print("Hey family!")
time.sleep(1)
print("It is time to generate the random numbers for the top and left axes of our grid!")
time.sleep(1)

def generate_random_numbers(team_name):
    print(f"Generating random numbers for the {team_name} axis...")
    nums = list(range(10))
    random.shuffle(nums)
    for num in nums:
        sys.stdout.flush()
        print(num, end=" ")
        time.sleep(0.5)
    print("")
    
generate_random_numbers("Kansas City Chiefs")
time.sleep(0.5)
generate_random_numbers("Philadelphia Eagles")