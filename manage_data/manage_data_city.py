import pandas as pd

class ManageDataCity:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManageDataCity, cls).__new__(cls)
            cls._instance.df_city = None
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        if self.df_city is None:
            self.df_city = pd.read_csv('./dataset/worldcities.csv')
            self.df_city = self.df_city[['city', 'country', 'lat', 'lng']]
            self.df_city['lat'] = self.df_city['lat'].astype(float)
            self.df_city['lng'] = self.df_city['lng'].astype(float)
            self.df_city['country'] = self.df_city['country'].replace('Spain', 'España')
            self.df_city['country'] = self.df_city['country'].replace('Mexico', 'México')
            self.df_city['country'] = self.df_city['country'].replace('Peru', 'Perú')
            self.df_city['city'] = self.df_city['city'].replace('Mexico City', 'Ciudad de México')

    def get_df_city(self):
        return self.df_city
    
    def merge_data(self, df):
        df_city = self.get_df_city()
        df_join = pd.merge(df, df_city, left_on=['ciudad', 'pais'], right_on=['city', 'country'], how='left')
        return df_join