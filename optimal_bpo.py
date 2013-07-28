"""
Optimal BPO is defined as the following:
    Cost is defined as the profit at current prices that could be made
    by using the research time to instead build floor(research_time/build_time) items

    The highest level at which the saving for that level will pay of the total cost of
    getting to that level in a year or less

    currently only works with capital parts cause production time is assumed to be 3.3h

    usage: API assumes s/ /_/ on input

    ~/D/evescripts> python optimal_bpo.py capital_shield_emitter
    Days to pay off 369.796686232
    Optimal ME 10

"""
import requests
import argparse

API_URL="http://linode.chlystyk.com:6969/item/{}?me={}"
PARTS_PER_DAY=7
def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('item')
    return parser.parse_args()

def main():
    args = parseargs()
    item = args.item
    time_to_pay_off = 0
    cost = 0
    current_me = 1
    previous_profit = requests.get(API_URL.format(item, 0)).json()['profit']
    while time_to_pay_off < 365:
        item_json = requests.get(API_URL.format(item, current_me)).json()
        next_level_profit = item_json['profit']
        profit_diff = next_level_profit - previous_profit
        cost += 4 * previous_profit
        time_to_pay_off = cost / profit_diff / PARTS_PER_DAY
        previous_profit = next_level_profit
        current_me = current_me + 1

    print "Days to pay off %s" % time_to_pay_off
    print "Optimal ME %s" % current_me


if __name__ == "__main__":
    main()

