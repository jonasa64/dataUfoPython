import analyze
import matplotlib.pyplot as plt
from datahandler import df
from html_temps import answrap

def main():

    with open('index.html', 'w+') as fp:
        fp.truncate(0)

        ans1, ans2 = analyze.sightings_where(df)
        html = answrap[0] + ans1 + answrap[1]
        html += answrap[0] + ans2 + answrap[1]

        plot, ans = analyze.sightings_when(df)
        html += answrap[0] + ans + answrap[1]

        plot.savefig('plot1.png')
        html += '\n <img src="plot1.png" alt="Plot1"> \n'

        ans = analyze.appearance(df)
        html += answrap[0] + ans + answrap[1]

        ans = analyze.duration(df)
        html += answrap[0] + ans + answrap[1]

        plot, _ = analyze.dayoftheweek(df)
        plot.savefig('plot2.png')
        html += '\n <img src="plot2.png" alt="Plot2"> \n'

        plot1, plot2 = analyze.sentiment_analyzis(df, 'sub')

        plot1.savefig('plot3-1.png')
        html += '\n <img src="plot3-1.png" alt="Plot3-1"> \n'

        plot2.savefig('plot3-2.png')
        html += '\n <img src="plot3-2.png" alt="Plot3-2"> \n'

        temp_html = analyze.state_map_plot(df)
        temp_html = temp_html.split("<body>", maxsplit=1)
        html = temp_html[0] + "<body>\n" + html + "\n" + temp_html[1]

        fp.write(html)


if __name__ == '__main__':
    main()
