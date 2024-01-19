if __name__ == '__main__':



    out_path = '/AntColony/konfigi/wyniki_csv/'
    from pea_utils import execute_from_ini_aco
    from AntColony.ACO import ACO
    # badanie schematów WG PARAMETRÓW DORIGO / ZESTAW 1
    # execute_from_ini_aco(ACO, '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/konfigi/badanie_schematow_dorigo'
    #                           '/test_DORIGO_CAS.ini')
    execute_from_ini_aco(ACO, '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/konfigi/badanie_schematow_dorigo'
                              '/test_DORIGO_DAS.ini')
    # badanie alfa | ZESTAW 2 ALFA > BETA
    execute_from_ini_aco(ACO, '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/konfigi/badanie_alfa_wieksza'
                              '/test_ALFA_CAS.ini')
    execute_from_ini_aco(ACO, '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/konfigi/badanie_alfa_wieksza'
                              '/test_ALFA_DAS.ini')

    # badanie beta | ZESTAW 3 BETA > ALFA
    execute_from_ini_aco(ACO, '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/konfigi/badanie_beta_wieksza'
                              '/test_beta_CAS.ini')
    execute_from_ini_aco(ACO, '/Users/sergiusz/PycharmProjects/pea-projekt/AntColony/konfigi/badanie_beta_wieksza'
                              '/test_beta_DAS.ini')
