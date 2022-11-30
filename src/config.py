class MapConfig:
    width=500
    height=500
    obstacle=[
        {"shape":"rectangle","center":(60,70),"width":30,"height":40},
        {"shape":"circle","center":(250,250),"radius":50},
        {"shape":"circle","center":(50,150),"radius":30},
        {"shape":"circle","center":(170,110),"radius":20}
    ]
    start=(50,100)
    end=(400,400)

class SolverConfig:
    population_size = 100       
    generation_number = 1000
    x_min = 0.0
    x_max = 500
    y_min = 0.0
    y_max = 500
    start_x = 50
    start_y = 100
    end_x = 400
    end_y = 400