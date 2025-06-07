import pandas as pd

class ConfigDTS:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigDTS, cls).__new__(cls)
            cls._instance.config = cls._load_config(cls)
            cls._instance.data = None
        return cls._instance
    
    def _load_config(self):
        return {
            'data_path': './dataset/Ventas_Minoristas.xlsx',
            'data_columns': ['id_cliente', 'nombre_producto', 'cantidad', 'precio_unitario',
                             'fecha', 'categoria', 'pais', 'ciudad', 'metodo_pago', 'edad_cliente',
                             'genero_cliente', 'calificacion_satisfaccion']
        }
    
    def get_config(self):
        return self.config
    
    def get_data(self):
        if self.data is None:
            data_read =  pd.read_excel(self.config['data_path'])
            data_read.columns = self.config['data_columns']
            data_read['venta_total'] = data_read['precio_unitario'] * data_read['cantidad']
            return data_read
        return self.data