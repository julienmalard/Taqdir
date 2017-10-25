

lugar = Lugar(lat=12.3, long=14.5, alt=499)

lugar.obt_datos(1990, 2040, rcp=8.5, rep=1, diario=True, mensual=False, pasado='NOAA', regenerar=True)

lugar.guardar_datos()

lugar.obt_datos()

lugar.cargar_datos('mi_csv.csv')

lugar.obt_datos(1990, 2040, rcp=8.5, rep=1, diario=True, mensual=False, pasado='NOAA', regenerar=True)
