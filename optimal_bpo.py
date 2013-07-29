"""
Optimal BPO is defined as the following:
    Cost is defined as the profit at current prices that could be made
    by using the research time to instead build floor(research_time/build_time) items

    The highest level at which the saving for that level will pay of the total cost of
    getting to that level in a year or less

    I will braindump some stuff here as I changed my mind on correctness a whole bunch.

    The script decides when the next level stops being worth it. It does not consider the
    profit difference that me0-1 brings when considering me2-3. Other wise you are accounting
    for the gained profit more than once. Yes that profit exists on each item you make but it
    does not get considered in the advantage of paying for the *next* level.

    Defaults are for Capital production parts

    usage: API assumes s/ /_/ on input

    ~/D/evescripts> python optimal_bpo.py capital_shield_emitter
    Days to pay off 369.796686232
    Optimal ME 10

"""
import requests
import argparse

API_URL="http://linode.chlystyk.com:6969/item/{}?me={}"
def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('item')
    parser.add_argument('-p', '--parts-per-day', type=float, default=7.27, dest="parts")
    parser.add_argument('-P', '--parts-per-level', type=float, default=4, dest="parts_per_level")
    return parser.parse_args()

def main():
    args = parseargs()
    item = args.item
    parts_per_day = args.parts
    parts_per_level = args.parts_per_level
    time_to_pay_off = 0
    cost = 0
    current_me = 1
    previous_profit = requests.get(API_URL.format(item, 0)).json()['profit']
    while time_to_pay_off < 365:
        item_json = requests.get(API_URL.format(item, current_me)).json()
        next_level_profit = item_json['profit']
        profit_diff = next_level_profit - previous_profit
        print previous_profit
        cost = parts_per_level * previous_profit
        time_to_pay_off = cost / profit_diff / parts_per_day
        previous_profit = next_level_profit
        current_me = current_me + 1
        print "profit diff:", profit_diff
        print "cost:", cost
        print "optimal me:", current_me
        print "days to pay off:" , time_to_pay_off

    print "Days to pay off %s" % time_to_pay_off
    print "Optimal ME %s" % current_me


if __name__ == "__main__":
    main()

