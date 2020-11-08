
import pandas as pd
import numpy as np
import plotly.express as px

class DataInterface:
    CUSTOMER_ID = 147
    N_NEIGHBOURS = 100

    def load_transactions(self):
        self.monthly_categories = pd.read_parquet('data/monthly_categories.parquet')
        self.neighbours = self.get_neighbours(self.N_NEIGHBOURS)
        self.my_categories = self.monthly_categories.loc[self.CUSTOMER_ID]
        self.neighbours_pie_data, self.neighbours_pie_colors = self.to_pie_data(self.neighbours.mean())
        self.my_pie_data, self.my_pie_colors = self.to_pie_data(self.my_categories)

    def transform_data(self):
        transactions = self.transactions
        account_grouped = transactions.groupby('tilinro')
        min_dates = account_grouped['maksupvm'].min()
        max_dates = account_grouped['maksupvm'].max()
        date_deltas = max_dates - min_dates
        transactions = self.transactions
        self.monthly_incomes = transactions.loc[transactions['category'] == 'Tulot'].groupby('tilinro')[
                              'rahamaara'].sum() / date_deltas.dt.days * 365 / 12
        self.my_transactions = transactions.loc[transactions['tilinro'] == self.CUSTOMER_ID]
        self.my_min_date = self.my_transactions['maksupvm'].min()
        self.my_max_date = self.my_transactions['maksupvm'].max()
        self.my_date_delta = self.my_max_date - self.my_min_date

    def get_neighbours(self, N):
        sorted_incomes = self.monthly_categories['Tulot'].sort_values()
        customer_ranking = sorted_incomes.index.get_loc(self.CUSTOMER_ID)
        neighbour_ids = sorted_incomes.iloc[customer_ranking - N:customer_ranking + N].index
        neighbours = self.monthly_categories.loc[neighbour_ids]
        return neighbours

    def to_pie_data(self, categories: pd.DataFrame):
        my_data_sorted = self.my_categories.drop('Tulot').sort_values()
        color_names = px.colors.sequential.Rainbow
        n_biggest = len(color_names)-1
        biggest_categories = my_data_sorted.iloc[:n_biggest].index
        other_categories = my_data_sorted.iloc[n_biggest:].index

        pie_data_biggest = -categories[biggest_categories]
        pie_data_other = -categories[other_categories].sum()
        pie_data_biggest['Muut'] = -categories['Muut'] + pie_data_other

        colors = {}
        for i, category in enumerate(biggest_categories):
            colors[category] = color_names[i]
        colors['Muut'] = len(biggest_categories)
        # colors['Muut'] = len(biggest_categories)
        pie_data_df = pd.DataFrame({'names': pie_data_biggest.index, 'values': pie_data_biggest.values})
        return pie_data_df, colors

    def to_histogram_data(self, category):
        neighbours = -self.neighbours[category]
        neighbours = neighbours.loc[(neighbours < neighbours.quantile(0.95)) & (neighbours > neighbours.quantile(0.05))]

        histogram_data = np.histogram(neighbours.values, bins='auto')
        colors = ['blue',] * len(histogram_data[1])
        for i, bar in enumerate(histogram_data[1]):
            if bar > -self.my_categories.loc[category]:
                colors[i] = 'red'
                break
        return histogram_data, colors
if __name__ == '__main__':
    di = DataInterface()
    di.load_transactions()
    neighbours = di.get_neighbours(100)
    print(neighbours.mean())