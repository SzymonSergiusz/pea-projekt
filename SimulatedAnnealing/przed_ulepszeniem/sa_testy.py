if __name__ == '__main__':
    import pea_utils
    import SA
    # !_ format outputu path, dist, czas, pamięć, jakość rozwiązania, długość_epok,
    #pea_utils.execute_from_ini_sa(SA.simulate_annealing,'ini/test_atsp_WzLosGeomPotDwa.ini')
    #pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'ini/test_atsp_WzLosLinMnDwa.ini')
    #pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'ini/test_atsp_WzLosLinPotDwa.ini')
    #pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'ini/test_atspwzorLosGeomMnozDwa.ini')
    #!_ dla temp = n^2
    #pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'ini/test_atsp_SimpleLosGeomPotDwa.ini')
    pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'ini/test_atsp_SimpleLosLinMnDwa.ini')
    pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'ini/test_atsp_SimpleLosLinPotDwa.ini')
    pea_utils.execute_from_ini_sa(SA.simulate_annealing, 'ini/test_atspSimpleLosGeomMnozDwa.ini')
