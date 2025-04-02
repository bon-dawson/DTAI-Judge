#!/usr/bin/env python3
"""
Player module for the "botwar ship" game.
"""
import copy
from typing import List
import math

from models.coordinate import Coordinate
from models.direction import Direction
from models.map import Map
from utils.constants import MISSILE_DAMAGE_ONE, MISSILE_DAMAGE_TWO


class Player:
    """
    Player class representing a team's ship in the game.
    """

    def __init__(self, team_id: int, missiles: int):
        """
        Initialize a player with the specified team ID.
        
        Args:
            team_id: Team ID (1-3)
        """
        self.team_id = team_id
        self.position = Coordinate(0, 0, 0)  # Will be set during game initialization
        self.previous_position = Coordinate(0, 0, 0)  # Track previous position for collision detection
        self.gold = 0
        self.shield = False
        self.alive = True
        self.missiles = missiles
        self.missiles_fired = []

    def move(self, direction: Direction, map: 'Map'):
        """
        Move the player in the specified direction.
        
        Args:
            direction: Direction to move in
        """
        if not self.alive:
            return

        # Store previous position before moving
        self.previous_position = Coordinate(self.position.q, self.position.r, self.position.s)

        new_position = self.position.next(direction)
        if map.is_valid_coordinate(new_position):
            self.position = new_position

    def fire_missile(self, target: Coordinate) -> bool:
        """
        Fire a missile at the specified target.
        
        Args:
            target: Target coordinate
            
        Returns:
            True if the missile was fired, False if no missiles left
        """
        if not self.alive or self.missiles <= 0:
            return False

        self.missiles -= 1
        self.missiles_fired.append(target)
        return True

    def collect_gold(self, amount: int):
        """
        Collect gold.
        
        Args:
            amount: Amount of gold to collect
        """
        if not self.alive:
            return

        self.gold += amount

    def equip_shield(self):
        """
        Equip a shield.
        """
        if not self.alive:
            return

        self.shield = True

    def hit_by_missile(self, count: int) -> int:
        """
        Apply the effect of being hit by missiles.
        
        Args:
            count: Number of missiles hit by
            
        Returns:
            Amount of gold lost
        """
        if count <= 0:
            return 0

        # Calculate gold lost based on missile count
        percentage = MISSILE_DAMAGE_ONE if count == 1 else MISSILE_DAMAGE_TWO  # 20% for 1 missile, 30% for 2+ missiles
        gold_lost = math.ceil(self.gold * percentage)

        self.gold -= gold_lost
        return gold_lost
