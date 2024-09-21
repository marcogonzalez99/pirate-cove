# -----------------------------------------------------------------------------------------

# | Pirate's Cove |

# -----------------------------------------------------------------------------------------

# Pirate Cove - A 2d Platformer Game

# Pitch: Take Back What Has Been Taken From You

# Audience: Everyone (Due to difficulty)

# Genre: 2d Platformer

# -----------------------------------------------------------------------------------------

# | Synopsis |

# -----------------------------------------------------------------------------------------

# Theme: Pirate Bay in the year 1650

# -----------------------------------------------------------------------------------------

# | Goal |

# -----------------------------------------------------------------------------------------

# Get to the Pirate Hat at the end of every stage

# Stomp on enemies, collect coins, collect the diamond in each level

# to attain the highest score, stealing back as much money as possible

# -----------------------------------------------------------------------------------------

# | Mechanics |

# -----------------------------------------------------------------------------------------

# | Jump | Allows the player to navigate platforms that are otherwise out of reach.

# | Coins | The player can collect coins to contribute to their score, which affects

# how much money is collected at the end of the game. The coins also will grant the player

# an extra life after collecting 100.

# | Diamonds | Diamonds are available for the player to collect that contributes to their

# score and greatly contributes to the total amount of money collected at the end of the

# game.

# | Lives | The player starts the game with 4 lives. Each time the player dies a life is

# taken away. Once the player reaches 0 lives, they get a game over and have to start

# over from the first level of the most recent world they completed.

# | Score | Everything the player does will add a set amount of points to their score

# this score at the end of the game will be converted into money.

# | Rank | At the end of the game, the player's score converts into money and that money

# will award the player with a rank. The ranks are F,D,C,B,A,A+,S

# -----------------------------------------------------------------------------------------

# | Uniqueness |

# -----------------------------------------------------------------------------------------

# Everything the player does in this game, contributes to stealing

# more money, allowing the player to retry levels in order to gain a higher score

# and in turn earning more money, which affects the players score at the end of the game

# -----------------------------------------------------------------------------------------

# The game comes in 6 states - Main_Menu, Tutorial, Overworld, Level, Game_Over, End_Game

# -----------------------------------------------------------------------------------------

# | Main Menu |

# -----------------------------------------------------------------------------------------

# The Main Menu is the starting state of the game, where the only option the player

# has is to press space to start the game

# -----------------------------------------------------------------------------------------

# | Tutorial |

# -----------------------------------------------------------------------------------------

# The Tutorial screen is for the user to understand how the game works and display the

# score values for the coins, diamonds, and defeating enemies

# -----------------------------------------------------------------------------------------

# | Overworld |

# -----------------------------------------------------------------------------------------

# The Overworld displays all the playable levels to the player, blacking out locked

# levels and displaying a hat to what level the player is currently on

# -----------------------------------------------------------------------------------------

# | Levels |

# -----------------------------------------------------------------------------------------

# The Level state is active whenever the user enters any unlocked level in the overworld

# Each level comes from terrain maps, that contains various coins, enemies, obstacles

# diamonds and a goal. Each level is custom made using the Tiled map editor

# -----------------------------------------------------------------------------------------

# | Game Over |

# -----------------------------------------------------------------------------------------

# The Game Over state is for when the player runs out of lives. Once the life counter

# hits zero, this state runs and the player has to hit "SPACE" to restart the game

# The way the checkpoints work, is that the player will restart back to the first level

# of the furthest world they have completed. If the player reaches world 2 and gets a game

# over, they will restart at World 2-1. The same applies for World 3, as well as the bonus

# world

# -----------------------------------------------------------------------------------------

# | End Game |

# -----------------------------------------------------------------------------------------

# End Game displays the results of all the things the player did during gameplay

# The game will display how many points they earned, how many coins they collected, how

# many diamonds they collected, and how many enemies they stomped on. Below these stats

# is a "Money Calculator" which will convert all the stats into currency. Based on the

# total amount of money earned, the player will be awarded with a letter grade to

# indicate how well the player performed. The ranks are as follows - F,D,C,B,A,A+,S

# -----------------------------------------------------------------------------------------

# | Technical Specifications |

# -----------------------------------------------------------------------------------------

# | Animations |

# -----------------------------------------------------------------------------------------

# At least three full animated Objects

# - Player (Pirate)

# - Background (Palm Trees)

# - Enemies

# - Coins and Diamonds

# - Overworld Nodes

#

# Scrolling Background or Three levels

# - 20 Levels in the game

# - Scrolling Background

# - Randomized Clouds in every level

# - Different Colored Backrground for World 1, World 2, World 3 and World X

# -----------------------------------------------------------------------------------------

# | Sound |

# -----------------------------------------------------------------------------------------

# Use background music/noise and

# triggered sounds

# - Main Menu Music

# - Credits Music

# - Game Over Music

# - Overworld Music

# - Different Background Music per Level

# - Level Complete Music

# - Player Fall Off Course Music

# - Player Died from Damage Music

# - Jump Sound sfx

# - Coin Collect sfx

# - Enemy Kill sfx

# - Diamond Collect sfx

# - Player Take Damage sfx

# -----------------------------------------------------------------------------------------

# | Visual |

# -----------------------------------------------------------------------------------------

# At least 3 elements of visual feedback

# for the user during gameplay

# - Score Tracker

# - Health Bar

# - Coins Collected

# - Diamonds Collected

# -----------------------------------------------------------------------------------------

# | Challenge |

# -----------------------------------------------------------------------------------------

# Demonstrate some means of dificulty scaling

# - Each World has 6 levels

# - Level 6 of each world is significantly more challenging

# - and the difficulty scales up as the player gets closer to the end of the world

# - World 3 is harder than World 2, and World 2 is harder than World 1

# -----------------------------------------------------------------------------------------

# | Theme |

# -----------------------------------------------------------------------------------------

# Theme that is clearly identifieable through sprites, backgrounds and sounds

# Clearly identifieable genre

# - Pirate theme through the player sprite and enemies

# - Treasure stealing game through coin and diamond sprite

# - Rock, Hard Sand, and Soft Sand terrain

# - The in-game music reflects the theme of the world, as well as whether or not

# - The player is playing a regular,bonus or challenge level

# - Player is playing a platformer game which is evident by the various

# - platforming challenges the game is based on

# -----------------------------------------------------------------------------------------

# | Game Assets |

# -----------------------------------------------------------------------------------------

# Graphics -

# Graphics obtained from Itch.io

# Pirates, Enemies, Coins and Rock Tiles obtained from:

# https://pixelfrog-assets.itch.io/treasure-hunters

# Diamonds, Hard Sand and Soft Sand obtained from:

# https://crusenho.itch.io/beriesadventureseaside

# Music

# All Music Grabbed from Various Nintendo Games. Ranging from the NES to the Switch

# -----------------------------------------------------------------------------------------

# | Easter Egg |

# -----------------------------------------------------------------------------------------

# If a level is too hard, try pressing F, T and L at the same time while in a level

# (P.S - Make sure you're on the ground :] )

# (P.P.S - This isn't free! So use it wisely)

# There is a 100,000 point fee for using this easter egg, which reduces your final score

# and total money collected by $1,000,000

# Be careful as this could lower your rank from an A to a B :]

# -----------------------------------------------------------------------------------------

# If you find yourself above the screen, look out for the grey arrow as it can help you

# find yourself

# -----------------------------------------------------------------------------------------
