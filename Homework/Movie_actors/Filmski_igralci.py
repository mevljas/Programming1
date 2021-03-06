import itertools


def igralci(povezave):
    return {oseba for oseba, film in povezave}

def filmi(povezave):
    return {film for oseba, film in povezave}

def filmi_igralca(igralec, povezave):
    return {film for oseba, film in povezave if oseba == igralec}

def igralci_filma(film, povezave):
    return {oseba for oseba, film_povezava in povezave if film == film_povezava}

def po_igralcih(povezave):
    return {oseba: filmi_igralca(oseba, povezave) for oseba, film in povezave}

def po_filmih(povezave):
    return {film: igralci_filma(film, povezave) for oseba, film in povezave}

def soigralci(igralci_filmi):
    return {tuple(sorted((igralec, igralec2))) for igralec2, filmi2 in igralci_filmi.items() for igralec, filmi in igralci_filmi.items() if (not len(filmi.intersection(filmi2)) == 0) and (not igralec == igralec2)}

def n_soigralcev(igralec, pari):
    return len({(ime1, ime2) for ime1, ime2 in pari if igralec in (ime1,ime2)})

def soigralci_igralca(igralec, pari):
    return {(ime1,ime2)[ime1 == igralec] for ime1, ime2 in pari if igralec in (ime1, ime2)}

def moc_povezave(igralec1, igralec2, povezave):
    return sum(2 / len(igralci_filma(film,povezave))**2 for film in filmi_igralca(igralec1, povezave).intersection(filmi_igralca(igralec2, povezave)))

def utezene_povezave(povezave):
    return {(par[0],par[1]): moc_povezave(par[0], par[1], povezave) for par in list(itertools.combinations(sorted(igralci(povezave)), 2))}

def povezani_z(igralec, pari):
    igralci = {igralec}
    mnozica_imen = set()
    isci = True
    while isci:
        isci = False
        for par in pari:
            mnozica_par = set(par)
            if not len(igralci.intersection(mnozica_par)) == 0 and not len(mnozica_par - igralci) == 0:
                igralci = igralci.union(mnozica_par)
                mnozica_imen = mnozica_imen.union(mnozica_par)
                isci = True
    return igralci


def otoki(pari):
    otoki = []
    povezani = set()
    if len(pari) > 0:
        ime1, ime2 = pari[0]
    else:
        return []
    povezani.add(ime1)
    povezani.add(ime2)
    isci = True
    while(isci):
        isci = False
        for par in pari:
            ime1, ime2 = par
            if (ime1 in povezani and ime2 not in povezani) or (ime2 in povezani and ime1 not in povezani):
                povezani.add(ime1)
                povezani.add(ime2)
                isci = True
    otoki.append(povezani)
    for ime1, ime2 in pari:
        par_mnozica = set()
        if ime1 not in povezani and ime2 not in povezani:
            par_mnozica.add(ime1)
            par_mnozica.add(ime2)
            otoki.append(par_mnozica)
    return otoki






import inspect
import ast
import unittest

class Test06(unittest.TestCase):
    povezave = [("Ana", "Od Čateža do Litije"),
                ("Berta", "Od Čateža do Litije"),
                ("Ana", "Harry Potter 4"),
                ("Cilka", "Harry Potter 4"),
                ("Berta", "Star Trek DS-9"),
                ("Dani", "Harry Potter 4"),
                ("Ema", "Star Trek DS-9"),
                ]

    def test_igralci(self):
        self.assertSetEqual(
            igralci(self.povezave), {"Ana", "Berta", "Cilka", "Dani", "Ema"})
        self.assertSetEqual(
            igralci(self.povezave[:2]), {"Ana", "Berta"})

    def test_filmi(self):
        self.assertSetEqual(
            filmi(self.povezave),
            {"Od Čateža do Litije", "Harry Potter 4", "Star Trek DS-9"})
        self.assertSetEqual(
            filmi(self.povezave[:2]), {"Od Čateža do Litije"})

    def test_filmi_igralca(self):
        self.assertSetEqual(
            filmi_igralca("Ana", self.povezave),
            {"Od Čateža do Litije", "Harry Potter 4"})

    def test_igralci_filma(self):
        self.assertSetEqual(
            igralci_filma("Harry Potter 4", self.povezave),
            {"Ana", "Cilka", "Dani"})

    def test_po_igralcih(self):
        self.assertDictEqual(
            po_igralcih(self.povezave),
            {"Ana": {"Od Čateža do Litije", "Harry Potter 4"},
             "Berta": {"Od Čateža do Litije", "Star Trek DS-9"},
             "Cilka": {"Harry Potter 4"},
             "Dani": {"Harry Potter 4"},
             "Ema": {"Star Trek DS-9"},
             })

    def test_po_filmih(self):
        self.assertDictEqual(
            po_filmih(self.povezave),
            {"Od Čateža do Litije": {"Ana", "Berta"},
             "Harry Potter 4": {"Ana", "Cilka", "Dani"},
             "Star Trek DS-9": {"Berta", "Ema"},
             }
        )


class Test07(unittest.TestCase):
    def test_soigralci(self):
        self.assertSetEqual(
            soigralci({"Ana": {"Od Čateža do Litije", "Harry Potter 4"},
                       "Berta": {"Od Čateža do Litije", "Star Trek DS-9"},
                       "Cilka": {"Harry Potter 4"},
                       "Dani": {"Harry Potter 4"},
                       "Ema": {"Star Trek DS-9"},
                         }),
            {("Ana", "Berta"), ("Ana", "Cilka"), ("Ana", "Dani"),
             ("Berta", "Ema"), ("Cilka", "Dani")}
        )

    def test_n_soigralcev(self):
        pari = {("Ana", "Berta"), ("Ana", "Cilka"), ("Ana", "Dani"),
                ("Berta", "Ema"), ("Cilka", "Dani")}

        self.assertEqual(n_soigralcev("Ana", pari), 3)
        self.assertEqual(n_soigralcev("Berta", pari), 2)
        self.assertEqual(n_soigralcev("Cilka", pari), 2)
        self.assertEqual(n_soigralcev("Dani", pari), 2)
        self.assertEqual(n_soigralcev("Ema", pari), 1)

    def test_soigralci_igralca(self):
        pari = {("Ana", "Berta"), ("Ana", "Cilka"), ("Ana", "Dani"),
                ("Berta", "Ema"), ("Cilka", "Dani")}

        self.assertEqual(soigralci_igralca("Ana", pari), {"Berta", "Cilka", "Dani"})
        self.assertEqual(soigralci_igralca("Berta", pari), {"Ana", "Ema"})
        self.assertEqual(soigralci_igralca("Cilka", pari), {"Ana", "Dani"})
        self.assertEqual(soigralci_igralca("Dani", pari), {"Ana", "Cilka"})
        self.assertEqual(soigralci_igralca("Ema", pari), {"Berta"})


class TestOneLine(unittest.TestCase):
    def is_one_line(self, *fs):
        for f in fs:
            self.assertIsInstance(
                ast.parse(inspect.getsource(f)).body[0].body[0],
                ast.Return,
                f"Funkcija {f.__name__} ni napisana v eni vrstici"
            )


class Test08(TestOneLine):
    def test_one_line(self):
        self.is_one_line(
            igralci, filmi, filmi_igralca, igralci_filma, po_igralcih,
            po_filmih, soigralci, n_soigralcev, soigralci_igralca)


class Test09(TestOneLine):
    povezave = [("Ana", "Od Čateža do Litije"),
                ("Berta", "Od Čateža do Litije"),
                ("Berta", "Harry Potter 4"),
                ("Ana", "Harry Potter 4"),
                ("Cilka", "Harry Potter 4"),
                ("Berta", "Star Trek DS-9"),
                ("Dani", "Harry Potter 4"),
                ("Ema", "Star Trek DS-9"),
                ]

    def test_moc_povezave(self):
        self.assertEqual(
            moc_povezave("Ana", "Berta", self.povezave), 2 / 2 ** 2 + 2 / 4 ** 2)
        self.assertEqual(
            moc_povezave("Ana", "Cilka", self.povezave), 2 / 4 ** 2)
        self.assertEqual(
            moc_povezave("Ana", "Ema", self.povezave), 0)
        self.assertEqual(
            moc_povezave("Cilka", "Dani", self.povezave), 2 / 4 ** 2)

    def test_utezene_povezave(self):
        self.assertDictEqual(
            utezene_povezave(self.povezave),
            {("Ana", "Berta"): 2 / 2 ** 2 + 2 / 4 ** 2,
             ("Ana", "Cilka"): 2 / 4 ** 2,
             ("Ana", "Dani"): 2 / 4 ** 2,
             ("Ana", "Ema"): 0,
             ("Berta", "Cilka"): 2 / 4 ** 2,
             ("Berta", "Dani"): 2 / 4 ** 2,
             ("Berta", "Ema"): 2 / 2 ** 2,
             ("Cilka", "Dani"): 2 / 4 ** 2,
             ("Cilka", "Ema"): 0,
             ("Dani", "Ema"): 0,
             }
        )

    def test_one_line(self):
        self.is_one_line(moc_povezave, utezene_povezave)


class Test10(unittest.TestCase):
    def test_povezani_z(self):
        pari = [("Ana", "Berta"), ("Berta", "Cilka"), ("Dani", "Ema"),
                           ("Berta", "Fanči"), ("Greta", "Helga")]
        self.assertSetEqual(
            povezani_z("Ana", pari), {"Ana", "Berta", "Cilka", "Fanči"})
        self.assertSetEqual(
            povezani_z("Berta", pari), {"Ana", "Berta", "Cilka", "Fanči"})
        self.assertSetEqual(
            povezani_z("Cilka", pari), {"Ana", "Berta", "Cilka", "Fanči"})
        self.assertSetEqual(
            povezani_z("Fanči", pari), {"Ana", "Berta", "Cilka", "Fanči"})

        self.assertSetEqual(
            povezani_z("Dani", pari), {"Dani", "Ema"})

        pari = [("Ana", "Berta"), ("Berta", "Cilka"), ("Dani", "Ema"),
                ("Berta", "Fanči"), ("Greta", "Helga"), ("Ema", "Fanči")]
        self.assertSetEqual(
            povezani_z("Ana", pari),
            {"Ana", "Berta", "Cilka", "Dani", "Ema", "Fanči"})
        self.assertSetEqual(
            povezani_z("Ema", pari),
            {"Ana", "Berta", "Cilka", "Dani", "Ema", "Fanči"})

    def test_otoki(self):
        o = otoki([("Ana", "Berta"), ("Berta", "Cilka"), ("Dani", "Ema"),
                   ("Berta", "Fanči"), ("Greta", "Helga")])
        self.assertEqual(len(o), 3)
        self.assertIn({"Ana", "Berta", "Cilka", "Fanči"}, o)
        self.assertIn({"Dani", "Ema"}, o)
        self.assertIn({"Greta", "Helga"}, o)

        o = otoki([("Ana", "Berta"), ("Berta", "Cilka"), ("Dani", "Ema"),
                   ("Berta", "Fanči"), ("Greta", "Helga"), ("Ema", "Fanči")])
        self.assertEqual(len(o), 2)
        self.assertIn({"Ana", "Berta", "Cilka", "Fanči", "Dani", "Ema"}, o)
        self.assertIn({"Greta", "Helga"}, o)

        self.assertEqual(
            otoki([("Ana", "Berta"), ("Berta", "Cilka"), ("Dani", "Ema"),
                   ("Berta", "Fanči"), ("Greta", "Helga"), ("Ema", "Fanči"),
                   ("Ana", "Helga")]),
            [{"Ana", "Berta", "Cilka", "Fanči", "Dani", "Ema", "Greta", "Helga"}]
        )
        self.assertEqual(otoki([]), [])


if __name__ == "__main__":
    unittest.main()

