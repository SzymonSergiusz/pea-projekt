if __name__ == '__main__':
    import pea_utils
    import SA

    badanie_chlodzenia = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_chlodzenia'
    badanie_epok = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_epok'
    badanie_t0 = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_t0'
    badanie_rozw = '/Users/sergiusz/PycharmProjects/pea-projekt/SimulatedAnnealing/ini/badanie_wyboru_rozwiazania'
    # test badanie chłodzenia
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_chlodzenia+'/test_wzor_los_geo_mnoz_dwazamiany.ini')
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_chlodzenia+'/test_wzor_los_log_mnoz_dwa_zamiany.ini')
    #
    #
    # #badanie epok
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_epok+'/test_wzor_los_geo_pot_luk.ini')

    #badanie t0
    # pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_t0+'/test_simple_los_geo_mnoz_luk.ini')

    #badanie wyboru rozwiązania
    #pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_rozw+'/test_wzor_los_geo_mnoz_dwazamiany.ini')
    #uzupelnienie
    #pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'uzupelnienie.ini')


    #?
    pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_chlodzenia+'/dodatkowe/test_wzor_los_geo_mnoz_dwazamiany.ini')
    pea_utils.execute_from_ini_sa(SA.simulate_annealing, badanie_chlodzenia+'/dodatkowe/test_wzor_los_log_mnoz_dwa_zamiany.ini')
