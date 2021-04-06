import matplotlib.pyplot as plt
from alpha_vantage.sectorperformance import SectorPerformances
import os


class Discovery():
    def alphav_sectors():
        """
        Return AlphaVantage Sectors
        """

        sp = SectorPerformances(
            key=os.getenv("API_KEY_ALPHAVANTAGE"), output_format="pandas"
        )
        data, meta_data = sp.get_sector()
        data['Rank A: Real-Time Performance'].plot(kind='bar')
        plt.title('Real Time Performance (%) per Sector')
        plt.tight_layout()
        plt.grid()
        #plt.show()
        return plt.show()
