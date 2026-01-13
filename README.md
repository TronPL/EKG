# System wspomagania analizy zapisu EKG (Holter)

Celem projektu jest stworzenie programu, który analizuje sygnał EKG
zarejestrowany przez urządzenie typu Holter i wskazuje fragmenty zapisu,
które powinny zostać sprawdzone przez lekarza.

Program nie stawia diagnozy medycznej – pełni rolę systemu wspomagania decyzji.

Wejście:
- plik CSV zawierający kolumny: time, voltage

Wyjście:
- lista przedziałów czasowych wymagających analizy (JSON)

Zastosowane metody:
- filtracja sygnału EKG
- detekcja załamków R
- analiza odstępów RR
- reguły eksperckie wykrywania anomalii rytmu
