import csv
import json

IN_FILE = '/home/deepakt/Downloads/EMAO2019614N.csv'
# IN_FILE = '/home/deepakt/Downloads/ao.csv'
# IN_FILE = '/home/deepakt/Downloads/RLA-MCA-Single-SessionFINAL.csv'


def main():
    with open(IN_FILE, 'rb') as fh:
        l_d_payload = []
        l_d_mycsv = csv.DictReader(fh, delimiter='|')
        for d_rec in l_d_mycsv:
            l_d_payload.append(d_rec)
        print json.dumps(l_d_payload)

if __name__ == '__main__':
    main()
