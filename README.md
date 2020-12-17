Kraken to aplikacja napisana w języku python3 do edycji plików binarnych
Została zaprojektowana pod zajęcia z Bezpieczeństwa Systemów i Usług Informatycznych.

Aplikacja została stworzona jako aplikacja interfejsu wiersza poleceń i oferuje 3 główne funkcjonalności:
	- Edycja pliku binarnego na podstawie wprowadzonego adresu oraz kolejnych bajtów
	- Generowanie reprezentacji pliku binarnego w formie adresu virtualnego, bajtów oraz ich konwersji na znaki ASCII
	- Generowanie asemblerowej reprezentacji kodu pliku binarnego
Implementacja obsługuje następujące typy plików binarnych:
	- ELF

Aplikacja wymaga niestandardowych bibliotek python'owych. List dostępna w pliku requirements.txt
Dla ułatwienia przygotowany został skrypt bash'owy prepare.sh, który tworzy virtualne środowisko i instaluje wymagane biblioteki

Aplikacja została zaprojektowana pod system Linux. Wsparcie dla systemu Windows powinno być możliwe, ale nie było to przetestowane

Użycie

Edycja pliku:

	./kraken.py ${binary_file} edit --address ${address} --bytes ${byte_1} ${byte_2}.. --output ${output_filename}
	np.
	./kraken.py crackme edit --address 0x8049d10 --bytes 1A 23 51 --output crackme2
Wyświetlanie bajtów pliku:

	./kraken.py ${binary_file} hexdump
	np.
	./kraken.py crackme hexdump
Wyświetlanie bajtów pliku:

	./kraken.py ${binary_file} disassemble
	np.
	./kraken.py crackme disassemble

Wszelkie podstawowe jak i opcjonalne argumenty są równierz dostępne w automatycznie wygenerowanej przez argparse pomocy

	./kraken.py --help

usage: kraken.py [-h] [--format {elf}] [--verbose]
                 file {hexdump,disassemble,edit} ...

positional arguments:
  file                  Binary file to parse

optional arguments:
  -h, --help            show this help message and exit
  --format {elf}, -f {elf}
                        Format of a binary e.g. elf
  --verbose, -v         Sets logging type to DEBUG

mode:
  {hexdump,disassemble,edit}
    hexdump             Parses file and prints its hexdump
    disassemble         Parses file and disassembles it
    edit                Changes data of a binary


