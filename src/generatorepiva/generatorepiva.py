import os
import csv
import random


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class GeneratorePiva():
    CODICI_STATISTICI_ENCODING = 'cp1252'
    CODICI_STATISTICI_FILENAME = os.path.join(CURRENT_DIR, 'blob/Codici-statistici-e-denominazioni-al-17_01_2023.csv')

    CODICE_PROVINCIA_KEY = 'Codice Provincia (Storico)(1)'


    def __init__(self) -> None:
        self._codici_statistici = set()

    def genera(self) -> str:
        """Generate a random "Partita IVA" (PIVA) number."""
        self._collect_codici_stastistici()

        # Generate a random number of 7 digits
        matricola = random.randint(1000000, 9999999)

        # Select a random code from "codici_statistici" list
        codice_statistico = random.sample(self._codici_statistici, 1)[0]

        # Compute the Luhn digit
        luhn_digit = self._compute_luhn_digit(int(str(matricola) + codice_statistico))

        # Return the PIVA
        return f'{matricola}{codice_statistico}{luhn_digit}'

    def _collect_codici_stastistici(self):
        """Collects the list of statistical codes from the CSV file"""
        if self._codici_statistici:
            return

        with open(self.CODICI_STATISTICI_FILENAME, encoding=self.CODICI_STATISTICI_ENCODING) as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                self._codici_statistici.add(row[self.CODICE_PROVINCIA_KEY])

    def _compute_luhn_digit(self, number):
        """Compute the Luhn digit for a given number."""
        def digits_of(n):
            return [int(d) for d in str(n)]

        number_with_zero = int(f'{number}0')
        digits = digits_of(number_with_zero)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]

        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))

        module = checksum % 10
        if module == 0:
            return 0
        return (10 - module)
