# Nokia Hackathon - Megoldások

A projekt a Nokia Hackathon feladatainak (Mágikus számok, Törésteszt, IPConfig Parser, Parkolás Díjszámító) refaktorált és optimalizált megoldásait tartalmazza. Az eredeti specifikációk a `TASKS.md` fájlban találhatók.

## Telepítés

A projekt letöltése (klónozása) a GitHub tárolóból az alábbi parancsokkal végezhető el:
```bash
git clone https://github.com/CsPS0/NOKIA-hackathon.git
cd NOKIA-hackathon
```

A projekt futtatásához Python környezet szükséges. A tesztelési modulok telepítése a projekt gyökérmappájában az alábbi paranccsal lehetséges:

```bash
pip install -r requirements.txt
```

## Futtatás

A feladatok futtatása központilag, a `run.py` parancssori (CLI) alkalmazáson keresztül történik.

Egy adott feladat indítása a `--task` paraméter megadásával lehetséges:
```bash
python run.py --task magic_numbers
python run.py --task drop_test
python run.py --task ipconfig_parser
python run.py --task parking_calculator
```

Az összes feladat egyidejű szekvenciális végrehajtásához, valamint az eredményfájlok (pl. `output.json`, `output.csv`) generálásához a `--all` kapcsoló alkalmazandó:
```bash
python run.py --all
```

## Tesztelés

A megoldások algoritmikus helyességének validációja automatizált integrációs tesztekkel történik. A tesztelési folyamat indítása:
```bash
pytest test_solutions.py
```

Az implementált architekturális (Clean Code) fejlesztésekről és optimalizációkról további technikai részletek a **[REFACTORING.md](REFACTORING.md)** dokumentumban olvashatók.
