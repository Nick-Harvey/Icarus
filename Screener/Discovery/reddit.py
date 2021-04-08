#import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from alpha_vantage.sectorperformance import SectorPerformances
import os


class Reddit():
    def alphav_sectors():
        """
        Return AlphaVantage Sectors
        """

        sp = SectorPerformances(
            key=os.getenv("API_KEY_ALPHAVANTAGE"), output_format="pandas"
        )
        data, meta_data = sp.get_sector()
        # data['Rank A: Real-Time Performance'].plot(kind='bar')
        # plt.title('Real Time Performance (%) per Sector')
        # plt.tight_layout()
        # plt.grid()
        fig = px.bar(data['Rank B: 1 Day Performance'])
        return fig
