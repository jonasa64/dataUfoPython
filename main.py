import analyze
import matplotlib.pyplot as plt
from datahandler import df

def main():
    analyze.sightings_where(df)

    plotfig, _, _ = analyze.sightings_when(df)
    plotfig.savefig('plot1.png')

    analyze.duration(df)

if __name__ == '__main__':
    main()
