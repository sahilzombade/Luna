"""
Sample File: sample2.py

Purpose:
Demonstrates a mixed-leg intraday strategy using the Luna framework.
This example showcases handling both option (CE) and future contracts simultaneously,
dynamic tracking based on tick time, and automated square-off logic.

Key Features Demonstrated:
1. Initialization of the MarketData loader.
2. Creation of a Strategy instance with target and stop-loss parameters.
3. Subscribing to multiple legs:
   - Long/short option contract (CE).
   - Short future contract.
4. Tick-by-tick simulation loop:
   - Advances one tick per iteration.
   - Updates all subscribed legs.
   - Dynamically starts tracking legs at a specified time (12:30:30).
   - Stops tracking and squares off all positions at a later time (14:30:00).
5. Computes and prints live and total PnL on each tick.
6. Final PnL reporting at the end of the simulation.

Usage Notes:
- Ensure that all required tick-level CSVs and precomputed dictionaries are available.
- Designed for intraday simulation; time-based triggers demonstrate conditional leg tracking.
- Can be used as a template for building strategies with mixed instrument types (options + futures).

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
strat.open_leg("RELIANCE28JAN212000CE", 5, "01012021")
strat.open_leg("RELIANCE", -5, "01012021", data_type = "future")


# -----------------------------
# Tick-by-tick simulation
# -----------------------------
while strat.is_active():
    strat.update_tick()  # advance one tick

    # -----------------------------
    # Example dynamic tracking based on tick time
    # -----------------------------
    current_tick = strat.current_tick_time
    
    # print(strat.get_latest_ltp("RELIANCE28JAN212000CE"))
    # print(strat.get_latest_ltp("RELIANCE"))

    if current_tick is not None and current_tick >= time(15, 29, 00):
        strat.stop_tracking_leg("RELIANCE28JAN212000CE")
        # strat.stop_tracking_leg("RELIANCE")
        strat.terminate_and_square_off()

    elif current_tick is not None and current_tick >= time(15, 28, 30):
        strat.start_tracking_leg("RELIANCE28JAN212000CE")
    
    
    elif current_tick is not None and current_tick >= time(15, 28, 00):
        strat.stop_tracking_leg("RELIANCE28JAN212000CE")
    

    elif current_tick is not None and current_tick >= time(15, 27, 30):
        strat.start_tracking_leg("RELIANCE28JAN212000CE")
        # strat.start_tracking_leg("RELIANCE")
        


    # -----------------------------
    # Access all info
    # -----------------------------
    # Active legs for PnL tracking
    active_legs = [(p.contract, p.qty, p.last_ltp, p.entry_price, p.live_pnl())
                   for c, p in strat.positions.items() if c in strat.active_legs]

    # Live and total PnL
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



