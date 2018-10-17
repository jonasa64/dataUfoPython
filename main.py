import analyze
import matplotlib.pyplot as plt
from datahandler import df

def main():
    analyze.sightings_where(df)

    plot, _, _ = analyze.sightings_when(df)
    plot.savefig('plot1.png')

    analyze.appearance(df)
    analyze.duration(df)

    plot, _ = analyze.dayoftheweek(df)
    plot.savefig('plot2.png')

    plot1, plot2 = analyze.sentiment_analyzis(df, 'sub')

    plot1.savefig('plot3-1.png')
    plot2.savefig('plot3-2.png')

if __name__ == '__main__':
    main()
