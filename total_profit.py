import requests
import argparse


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('item')
    parser.add_argument('-m', '--mat-eff', dest='me', type=int, default=0)
    parser.add_argument('-p', '--part-eff', dest='part_me', type=int, default=0)
    return parser.parse_args()



def main():
    args = parseargs()
    me = args.me
    part_me = args.part_me
    item = args.item

    item_json = requests.get('http://linode.chlystyk.com:6969/item/{}?me={}&part_me={}'.format(item, me, part_me)).json()

    original_cost = item_json['cost']
    minsell = item_json['minsell']

    extra_profit = 0
    for part in item_json['parts']:
        profit = part['quantity'] * part['part']['profit']
        name = part['name']
        if profit < 0:
            print "Item {} is not profitable with a total loss of {}".format(name, profit)
        else:
            print "For item {} extra profit is {}".format(name, profit)
            extra_profit += profit

    print "Original Cost: {}".format(original_cost)
    print "Total Extra Profit: {}".format(extra_profit)
    print "At minsell: {} New Profit: {}".format(minsell, minsell - (original_cost - extra_profit))

if __name__ == "__main__":
    main()
