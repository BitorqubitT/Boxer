from sc2.bot_ai import BotAI  # parent class we inherit from
from sc2.data import Difficulty, Race  # difficulty for bots, race for the 1 of 3 races
from sc2.main import run_game  # function that facilitates actually running the agents in games
from sc2.player import Bot, Computer  #wrapper for whether or not the agent is one of your bots, or a "computer" player
from sc2 import maps  # maps method for loading maps to play in.
from sc2.ids.unit_typeid import UnitTypeId
import random

# Future Ideas:
# Scout enemy and build a map of unit and possibilites + counters?
# Start off with a build order, after that maintain rules.
# Function which does a search for units and the required upgrades/buildings
# If anything is missing it will build everything
# Tree?
# How does scouting work and how does it collect dat
# BUILD SC2 match analyzer
# Script which runs the main script and collects the data(mine and the opponents)

# TODO:
# Put build orders in a file or maybe just a list.
# Read file and try to follow this build orders.

# Give attack order with all my fighting units ( is there a function to check these?

# Create a functions which finds the best build positions.


# How do I deal with build order at the same time.
# What data structure do I use here?
# HASHTABLE?
# Lets use the function names here instead of a string describing the function.

build_order = {
        14: SUPPLYDEPOT,
        15: BARRACKS,
        16: REFINERY,
        20: COMMANDCENTER
        }


"""
We take in a build order, unitcount + order_name
Then we check the current unitcount
If unit count is found then we build then we pop this item from the dictionary.
"""

def build_order_follower(build_order, supply_used):
    if build_order.get(self.supply_used) is None:
        return None
    else:
        return build_order.get(supply_used)
    


# if build_order_follower(build_order, self.supply_used) is not None:
# Check if building or unit
# build it


# I need a test version somewhere lawl.


class IncrediBot(BotAI): # inhereits from BotAI (part of BurnySC2)
    async def on_step(self, iteration: int): # on_step is a method that is called every step of the game.
        print(f"{iteration}, n_workers: {self.workers.amount}, n_idle_workers: {self.workers.idle.amount},", \
            f"minerals: {self.minerals}, gas: {self.vespene}, reapers: {self.structures(UnitTypeId.REAPER).amount},", \
            f"BARRACKS: {self.structures(UnitTypeId.BARRACKS).amount}, supply: {self.supply_used}/{self.supply_cap}")
        
        await self.distribute_workers() # put idle workers back to work

        if self.townhalls:  # do we have a commandcenter?
            commandcenter = self.townhalls.random  # select one (will just be one for now)

            # if we have less than 10 Marines, build one:
            if self.structures(UnitTypeId.MARINE).amount < 60 and self.can_afford(UnitTypeId.MARINE):
                for sg in self.structures(UnitTypeId.BARRACKS).ready.idle:
                    if self.can_afford(UnitTypeId.MARINE):
                        sg.train(UnitTypeId.MARINE)
            
            #Build reapers
            if self.structures(UnitTypeId.REAPER).amount < 10 and self.can_afford(UnitTypeId.REAPER):
                for sg in self.structures(UnitTypeId.BARRACKS).ready.idle:
                    if self.can_afford(UnitTypeId.REAPER):
                        sg.train(UnitTypeId.REAPER)

            # leave room to build stuff
            supply_remaining = self.supply_cap - self.supply_used
            if commandcenter.is_idle and self.can_afford(UnitTypeId.SCV) and supply_remaining > 4:
                commandcenter.train(UnitTypeId.SCV)
            

            # Maybe I can remove this line since I have a different rule for building supplydepots
            elif not self.structures(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) == 0:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=commandcenter)
           
         """
            elif self.structures(UnitTypeId.BARRACKS).amount < 3:
                if self.can_afford(UnitTypeId.BARRACKS):  # and we can afford one:
                    # build one near the Pylon that is closest to the nexus:
                    await self.build(UnitTypeId.BARRACKS, near=self.structures(UnitTypeId.SUPPLYDEPOT).closest_to(commandcenter))
         """
            
            # Do I want to keep calling this function? 
            # If this unittype.object isnt allowed then put it in the dict

            build_next = build_order_follower(build_order, self.supply_used)
            
            # Maybe create a function that check all variables and then returns wait ....................
            if build_next is not None:
                if self.can_afford(UnitTypeId.build_next):
                   await self.build(UnitTypeId.build_next, near=commandcenter)

            if supply_remaining <= 2:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    await self.build(UnitTypeId.SUPPLYDEPOT, near = commandcenter)

            if self.units(UnitTypeId.MARINE).amount >= 15:
                if self.enemy_units:
                    for vr in self.units(UnitTypeId.MARINE).idle:
                        vr.attack(random.choice(self.enemy_units))

                elif self.enemy_structures:
                    for vr in self.units(UnitTypeId.MARINE).idle:
                        vr.attack(random.choice(self.enemy_structures))
               
                else:
                    for vr in self.units(UnitTypeId.MARINE).idle:
                        vr.attack(self.enemy_start_locations[0])

            if self.units(UnitTypeId.REAPER).amount >= 5:
                if self.enemy_units:
                    for vr in self.units(UnitTypeId.REAPER).idle:
                        vr.attack(random.choice(self.enemy_units))
                
                elif self.enemy_structures:
                    for vr in self.units(UnitTypeId.REAPER).idle:
                        vr.attack(random.choice(self.enemy_structures))
                
                else:
                    for vr in self.units(UnitTypeId.REAPER).idle:
                        vr.attack(self.enemy_start_locations[0])


run_game(  # run_game is a function that runs the game.
    maps.get("testmap"), # the map we are playing on
    [Bot(Race.Terran, IncrediBot()), # runs our coded bot, protoss race, and we pass our bot object 
     Computer(Race.Zerg, Difficulty.Hard)], # runs a pre-made computer agent, zerg race, with a hard difficulty.
    realtime=False, # When set to True, the agent is limited in how long each step can take to process.
)
