# PBL-3-Citymapper


#Presentation:
#-no code and +++ demo
#- 7min

# **📦 \[Project Name]**



**MVP Status:** 

v1.0-Production

**Group Members:** 

Yousef Abouturkia, Charlie Delecour, Simon Berger


## **🎯 Project Overview**

LowBid is an interactive auction simulator where the player with the lowest unique bid wins. Instead of paying the highest amount, you pay the lowest price that nobody else bid. Placing bids costs money, so you have to be strategic.
The system uses a Binary Search Tree (BST) to efficiently manage bids, multiple AI strategies to simulate different bidding behaviors, and a simulation engine to analyze how different cost functions affect gameplay.


Key Features:

- Interactive auction rounds with real-time bid tracking
- AI players with different strategies (CHeapstake,Diceroller...)
- Human vs. bot gameplay
- Multi-round simulation with performance analytics
- BST explorer tool to understand tree structure

## **🚀 Quick Start (Architect Level: < 60s Setup)**

Instructions on how to get this project running on a fresh machine.

1. **Clone the repo:**\
   git clone (https://github.com/simonshg06/PBL2-Auction-site.git)
   cd \[project-folder]

2. **Setup Virtual Environment:**\
   python -m venv .venv\
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. **Install Dependencies:**\
   pip install -r requirements.txt

4. **Run Application:**\
   python main.py


## **🛠️ Technical Architecture**

Explain how your code is organized. An "Architect-level" README should describe the separation of concerns.

The code is organized into five main modules with clear separation of concerns:

1. BST.py (Data Structure)

Purpose: Efficiently stores and organizes all bids by price
How it works:

-Prices are organized in a tree where lower prices go left, higher prices go right
-Multiple players can bid the same price, they're stored in a list at that price node
-Inorder traversal gives sorted bids from lowest to highest price


Key Methods:

insert(price, player)--> Add a new bid to the tree
find_lowest_unique() --> Find the first price with exactly one bidder (the winner)
successor(price) / predecessor(price) --> Find next higher/lower price in tree
delete_player_bid(price, player) --> Remove a player's bid




2. auction.py — Single Auction Round

Purpose: Runs one round of bidding and determines the winner
How it works:

-Creates a new BST for this round
-Players place bids one at a time
-Tracks the cost each player pays 
-Calculates seller revenue (sum of all bid costs)
-Finds and announces the winner


Key Methods:

place_bid(player, price) —-> Add a player's bid and update their cost
load_from_csv(filepath) —-> Load bids from a CSV file
resolve() —-> Find the lowest unique bid winner
summary() —-> Print auction results nicely formatted
analysis() —-> Return statistics about the round



3. strategies.py — AI Bidding Strategies

Purpose: Define different ways players choose their bids
Four Bot Types:

DiceRoller —-> Bids randomly
Cheapskate —-> Prefers low prices (exponential bias toward 0)
Accountant —-> Maximizes profit 
Historian —-> Analyzes winning bids from previous rounds 
Human —-> Real player input with cost reference display




4. simulation.py — Multi-Round Simulation Engine

Purpose: Run hundreds of rounds automatically and collect statistics

How it works:

-Runs rounds with the same players
-Tracks wins, spending, and profit for each player
-Compares different cost function parameters (alpha values)


Key Methods:

run(n_rounds) — Execute multiple rounds
report() — Print detailed statistics and rankings
compare_parameters(alpha_values) — Test different cost formulas



5. main.py — Interactive Menu & Demos

Purpose: User-facing interface with 4 interactive options

Menu Options:

-Demo Round 
-BST Explorer 
-Auto Simulation 
-Human vs Bots 



## **🧪 Testing & Validation**

How can a user verify the code works?

Run python main.py and try each menu option:

Demo Round —-> players bid randomly. Check that the winner has a unique bid.
BST Explorer —-> Query a price and verify successor/predecessor show correct next prices.
Simulation —->Run 100 rounds.
Human vs Bots —-> Play 5 rounds. Verify costs decrease as you bid higher .


## **📦 Dependencies**

List the main third-party libraries used and _why_ they were chosen:

- csv — Read bid data from CSV files
- random — Generate random bids and weighted choices
- math — Calculate exponential weights for strategies
- dataclasses — Define clean PlayerStats structure 


## **🔮 Future Roadmap (v2.0)**

What features would you add if you had more time or a larger budget?
- Creating an intetrface 
- Custom Rules Engine, details on what users can adjust (base cost, alpha, max price...)
- Visualization Dashboard, charts: win rates, revenue trends, leaderboard...
