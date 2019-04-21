###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b


# This is a helper function that will fetch all of the available 
# partitions for you to use for your brute force algorithm.
def get_partitions(set_):
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    trip,trips= [],[]
    cowCopy = cows.copy()
    while cowCopy != {}: #check if the resulting dictionary is empty, if empty no more operation required
        limitCheck = 0
        cowss = cowCopy.copy()
        trip = []
        indx = 0
        
        while cowss != {}:
            if limitCheck+max(cowss.values()) <= limit:
                limitCheck += max(cowss.values())
                '''
                when making dictionary's keys and values a list, the list of keys and list of the values
                will have same index
                '''
                indx = list(cowss.values()).index(max(cowss.values()))
                trip.append(list(cowss.keys())[indx])
                del cowCopy[list(cowss.keys())[indx]] #delete the maximum weight entry of cow
                del cowss[list(cowss.keys())[indx]] #delete the maximum weight entry of cow
#                print(cowss.keys(), cows.values())
            else:
                indx = list(cowss.values()).index(max(cowss.values()))
                del cowss[list(cowss.keys())[indx]] #delete the maximum weight entry of cow
        
        trips.append(trip)
        
    return trips



# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    
#    partn = []
    partn = {}
    for partition in get_partitions(list(cows.keys())):
#        partn.append(partition)
        if not(len(partition) in partn.keys()):
            partn[len(partition)] = []
            (partn[len(partition)]).append(partition)
        else:
            (partn[len(partition)]).append(partition)
    
    for ntrips in partn.keys():
        '''
        ntrips = key, the value that coresponds to the number of trips taken by spaceship
        '''
        for atrip in partn[ntrips]:
            '''
            selects one of the trips that is, at start, the number of trips is one
            on next loop, the number of trips is two and all the possible combination
            of the cows for two trips journey and so on
            '''
            count = 0 #to count the number of trips that is supposed to be made in this trip
            for trip in atrip:
                '''
                -atrip is the list of different trips that will have to be taken for particular
                ntrips
                -trip is the ist of cows that are in each trip
                '''
                limitCheck = 0
                for cow in trip:
                    '''
                    trip is a list that stores the name o cows in each trip
                    '''
                    limitCheck += cows[cow] #to check the weight of cows in each trip
                if limitCheck > limit: #check if the weight in each trip exceeds the limit
                    continue #if it exceeds, break this loop and stop checking this combination
                else:
                    count += 1
                if count == len(atrip):
                    return atrip

# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
print(cows)

print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))


