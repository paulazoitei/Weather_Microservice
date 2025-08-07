import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class TemperaturesChart:
    @staticmethod
    def create_plot(city_name, dates, temperatures):
        try:
            fig, ax = plt.subplots(figsize=(9, 6))
            ax.set_xlabel("Dates from 1 to 5 august", fontsize=12)
            ax.set_ylabel("Temperatures")
            ax.set_title(f"Temperature fluctuation chart for {city_name}")
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

            ax.plot(dates, temperatures, linestyle='--', marker='o', color='red')
            plt.show()
        except Exception as e:
            print(f" Error generating chart:{e}")