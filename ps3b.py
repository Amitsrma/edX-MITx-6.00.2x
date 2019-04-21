# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab
from ps3b_precompiled_35 import *
#random.seed(0)

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """
    
'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

        # TODO

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        # TODO
        if random.random() < self.clearProb:
            return True
        else:
            return False

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        # TODO
        excepn = NoChildException()
        if self.maxBirthProb == 1.0:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        elif random.random() < self.maxBirthProb * (1-popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            return excepn


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.popDensity = len(self.viruses)/self.maxPop


    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        # TODO
        return (len(self.viruses))
        

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        # TODO
        AllViruses = self.viruses.copy()
        for virus in AllViruses:
            if len(self.viruses) == self.maxPop:
                break
            try:
                if (virus.doesClear()):
                    self.viruses.remove(virus)
                else:
                    offspring = virus.reproduce(self.popDensity)
                    if not(isinstance(offspring,NoChildException)):
                        self.viruses.append(virus.reproduce(self.popDensity))
            except:
                pass
        self.popDensity = len(self.viruses)/self.maxPop
        return len(self.viruses)        

# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
    time, pop_size = range(300),[]
    for i in range(300):
        pop_size.append(0)
    step = 0
    for i in range(numTrials):
        viruses = []
        for i in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        #print(len(viruses))
        patient = Patient(viruses, maxPop)
        #print(patient.getTotalPop())

        for timesteps in range(300):
            if patient.getTotalPop()<=maxPop:
                patient.update()
#            if timesteps<15:
            #print(patient.getTotalPop(),end = '\t')
            pop_size[timesteps] += patient.getTotalPop()/numTrials
            step += 1


    pylab.plot(time, pop_size)
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.title('SimpleVirus simulation')
    #pylab.legend('A P')
    return pop_size
    #return(time[:15], pop_size[:15])



#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        # TODO
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb
#        self.maxBirthProb = maxBirthProb
#        self.clearProb = clearProb
        #self.sv = SimpleVirus.__init__(self, self.maxBirthProb, self.clearProb)
        self.resistances = resistances



    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO
        try:
            return self.resistances[drug]
        except:
            return False



    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # TODO
        excepn = NoChildException()
        self.popDensity = popDensity
        res = {}
        if self.resistances == {}:
            if random.random() < SimpleVirus.getMaxBirthProb(self)*(1-self.popDensity):
                for i in self.resistances.keys():
                    if random.random() < (1-self.mutProb):
                        res[i] = self.resistances[i]
                    else:
                        res[i] = not(self.resistances[i])
                return ResistantVirus(SimpleVirus.getMaxBirthProb(self), SimpleVirus.getClearProb(self), res, self.mutProb)
        elif all(self.resistances[i] == True for i in activeDrugs):
            if random.random() < SimpleVirus.getMaxBirthProb(self)*(1-self.popDensity):
                for i in self.resistances.keys():
                    if random.random() < (1-self.mutProb):
                        res[i] = self.resistances[i]
                    else:
                        res[i] = not(self.resistances[i])
                return ResistantVirus(SimpleVirus.getMaxBirthProb(self), SimpleVirus.getClearProb(self), res, self.mutProb)
        else:
            return excepn
            raise excepn


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        # TODO
        Patient.__init__(self, viruses, maxPop)
        self.rviruses = Patient.getViruses(self)
        self.rmaxPop = Patient.getMaxPop(self)
        self.drugs = []
        """
        rpopDensity: the population density of resistant viruses
        """
        self.rpopDensity = len(Patient.getViruses(self))/Patient.getMaxPop(self)




    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        if not(newDrug in self.drugs):
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO
        self.resist = []
#        for i in self.drugs:
#            if i in drugResist and not(i in self.resist):
#                self.resist.append(i)
#        return len(self.rviruses)
        resistantNos = 0
        for virus in self.rviruses:
            virCheck = all(virus.isResistantTo(drug) for drug in drugResist)
            if virCheck:
                resistantNos += 1
        return resistantNos
                

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        # TODO
        allViruses = self.rviruses.copy()
        for virus in allViruses:
            #print(virus)
            if (virus.doesClear()):
                self.rviruses.remove(virus)
            else:
                offspring = virus.reproduce(self.rpopDensity, self.drugs)
                if isinstance(offspring, ResistantVirus) or isinstance(offspring, SimpleVirus):
                    self.rviruses.append(offspring)

        self.rpopDensity = len(self.rviruses)/Patient.getMaxPop(self)
        
        return len(self.viruses)

#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    # TODO

    Total = []
    TotalGutt = []
    for i in range(300):
        Total.append(0)
        TotalGutt.append(0)

    for trials in range(numTrials):
        viruses = []
        for i in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        patient = TreatedPatient(viruses, maxPop)

        for step in range(0,150):
            if patient.getTotalPop() <= maxPop:
                patient.update()
            Total[step] += patient.getTotalPop()
            TotalGutt[step] += patient.getResistPop(['guttagonol'])

        patient.addPrescription('guttagonol')

        for step in range(150,300):
            if patient.getTotalPop() <= maxPop:
                patient.update()
            Total[step] += patient.getTotalPop()
            TotalGutt[step] += patient.getResistPop(['guttagonol'])

#    for i in range(300):
#        Total[step] /= numTrials
#        TotalGutt[step] /= numTrials

    timestep = range(300)
    #return len(timestep), len(final), final[:15]
    pylab.plot(timestep, Total, color = 'b')
    pylab.plot(timestep, TotalGutt, color = 'r')
    return Total, TotalGutt



#    allResults = []
#    allgutt = []
#    timestep = range(1,301)
#    for trials in range(numTrials):
#        viruses = []
#        for i in range(numViruses):
#            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
#        patient = TreatedPatient(viruses, maxPop)
#        
#        pop = []
#        guttpop = []
#
#        for step in range(1,151):
#            if patient.getTotalPop() <= maxPop:
#                patient.update()
#            pop.append(patient.getTotalPop())
#            guttpop.append(patient.getResistPop(['guttagonol']))
#        patient.addPrescription('guttagonol')
#        
#        for step in range(1,151):
#            if patient.getTotalPop() <= maxPop:
#                patient.update()
#            pop.append(patient.getTotalPop())
#            guttpop.append(patient.getResistPop(['guttagonol']))
#        allResults.append(pop)
#        allgutt.append(guttpop)
#    final = []
#    finalgutt = []
#    for i in range(300):
#        avg = 0
#        avggutt = 0
#        for j in range(numTrials):
#            avg += allResults[j][i]
#            avggutt += allgutt[j][i]
#        final.append(avg/numTrials)
#        finalgutt.append(avggutt/numTrials)
#    timestep = range(300)
#    #return len(timestep), len(final), final[:15]
#    pylab.plot(timestep, final, color = 'b')
#    pylab.plot(timestep, finalgutt, color = 'r')
#    return final, finalgutt
        
        

    
#    for trials in range(numTrials):
#        viruses = []
#        for i in range(numViruses):
#            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
#        patient = TreatedPatient(viruses, maxPop)
#        time = []
#        step = 0
#        virusSize = []
#        for i in range(150):
#            patient.update()
#            step += 1
#            time.append(step)
#            virusSize.append(patient.getTotalPop())
#        pylab.plot(time, virusSize, color = 'b')
#        patient.addPrescription('guttagonol')
#        viruses = []
#        for i in range(numViruses):
#            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
#        patient = TreatedPatient(viruses, maxPop)
#        patient.addPrescription('guttagonol')
#        time = []
#        step = 0
#        virusSize = []
#        for i in range(150):
#            patient.update()
#            step += 1
#            time.append(step)
#            virusSize.append(patient.getTotalPop())
#        pylab.plot(time, virusSize, color = 'r')
#            
