"""
Sample File: sample1.py

Purpose:
Demonstrates a basic intraday strategy using the Luna framework.
This example showcases subscribing to option contracts, starting PnL tracking,
and performing tick-by-tick simulation for live PnL computation.

Key Features Demonstrated:
1. Initialization of the MarketData loader.
2. Creation of a Strategy instance with target and stop-loss parameters.
3. Subscribing to multiple option legs (CE and PE) with negative quantity (short position).
4. Starting PnL tracking for subscribed legs.
5. Tick-by-tick simulation loop:
   - Advances one tick per iteration.
   - Updates all subscribed legs.
   - Computes and prints live and total PnL.
   - Maintains a history of realized and unrealized PnL.
6. Final PnL reporting at the end of the simulation.

Usage Notes:
- Ensure that all required data (tick CSVs and precomputed dictionaries) are available.
- Run the script as a standalone Python file.
- Designed for intraday simulation; actual timestamps are based on the data loaded from the MarketData loader.
- This sample can be used as a template to create custom strategies by modifying legs, quantities, and tracking logic.

Author:
Luna Framework Development Team
"""



from core import *
from fetchers import * 
from Precomputed import *

# -----------------------------
# Initialize market data
# -----------------------------
md = MarketData()

# -----------------------------
# Create strategy
# -----------------------------
strat = Strategy("TestStrat", md, target=200, sl=-200)

# -----------------------------
# Subscribe / register all legs
# -----------------------------
strat.open_leg("RELIANCE28JAN212000CE", -3, "01012021")
strat.open_leg("RELIANCE28JAN212000PE", 5, "01012021")

# -----------------------------
# Start tracking CE/PE immediately
# -----------------------------
strat.start_tracking_leg("RELIANCE28JAN212000CE")
strat.start_tracking_leg("RELIANCE28JAN212000PE")

# -----------------------------
# Tick-by-tick simulation 
# -----------------------------
while strat.is_active():
    strat.update_tick()  # advance one tick

    
    # -----------------------------
    # Access all info
    # -----------------------------

    # Active legs for PnL tracking
    active_legs = [(p.contract, p.qty, p.last_ltp, p.entry_price, p.live_pnl())
                   for c, p in strat.positions.items() if c in strat.active_legs]

    # Live and total PnL
    current_tick = strat.current_tick_time
    live_pnl = strat.live_total_pnl()
    total_pnl = strat.total_pnl()
    realized_pnl = strat.realized_pnl

    # Print tick info
    print("----- Tick Info -----")
    print(f"Current Tick Time : {current_tick}")
    print(f"Active Legs       : {active_legs}")
    print(f"Live PnL          : {live_pnl:.2f}")
    print(f"Realized PnL      : {realized_pnl:.2f}")
    print(f"Total PnL         : {total_pnl:.2f}")
    print(f"Strategy Active   : {strat.is_active()}")
    print("--------------------\n")

# -----------------------------
# Print final results
# -----------------------------
print(f"Final Total PnL: {strat.total_pnl():.2f}")

