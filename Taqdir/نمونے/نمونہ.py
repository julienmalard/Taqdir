from ..مقام import مقام
from ..Predictores.Observados import Observado

lugar = مقام(lat=12.3, long=14.5, elev=499)

obs = Observado('.csv')

lugar.prep_datos(1990, 2040, rcp=8.5, n_rep=1, diario=True, mensual=False, postdict='NOAA', regenerar=True)

lugar.guardar_datos()

lugar.cargar_datos('mi_csv.csv')

lugar.prep_datos(1990, 2040, rcp=8.5, n_rep=1, diario=True, mensual=False, postdict='NOAA', regenerar=True)
