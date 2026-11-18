@echo off
setlocal
chcp 65001 >nul

REM Extrahiert OSM-Daten (Verkehr, Versorgungs-POIs, Landnutzung) fuer den
REM Raum Aachen/Eifel/Simmerath in ein GeoPackage. Benoetigt ogr2ogr (GDAL).

REM --- HILFE ---
if "%~1"=="" goto :hilfe
if /i "%~1"=="/?" goto :hilfe
if /i "%~1"=="-h" goto :hilfe
if /i "%~1"=="--help" goto :hilfe

REM --- KONFIGURATION (aus Argumenten) ---
set "INPUT_OSM=%~f1"
if "%~2"=="" (set "ZIEL_ORDNER=%~dp0") else (set "ZIEL_ORDNER=%~f2")
if "%ZIEL_ORDNER:~-1%"=="\" set "ZIEL_ORDNER=%ZIEL_ORDNER:~0,-1%"
set "OUTPUT_GPKG=%ZIEL_ORDNER%\Simmerath_Analyse_Stabil.gpkg"
set "TEMP_RAW_GPKG=%ZIEL_ORDNER%\temp_raw_data.gpkg"

if not exist "%INPUT_OSM%" (
    echo FEHLER: OSM-Datei nicht gefunden: "%INPUT_OSM%"
    echo.
    goto :hilfe
)

REM --- DER SICHERE BEREICH (BOUNDING BOX) ---
REM Koordinaten ca.: West(5.9) Sud(50.3) Ost(6.8) Nord(51.0)
REM Deckt ab: Aachen, Simmerath, Monschau, Roetgen, Stolberg, Heimbach, Schleiden
set "BBOX=5.9 50.3 6.8 51.0"

if not exist "%ZIEL_ORDNER%" mkdir "%ZIEL_ORDNER%"

echo --- START: Analyse Simmerath (v6 - Stabil-Modus) ---

REM 0. AUFRAEUMEN
if exist "%TEMP_RAW_GPKG%" del "%TEMP_RAW_GPKG%"

REM 1. GROSSER EXPORT (Rechteck statt Polygon)
echo [1/3] Lese OSM-Daten im Rechteck (Aachen-Eifel)...
echo ... Das ist absturzsicher, dauert aber immer noch etwas ...

REM -spat xmin ymin xmax ymax (Raumlicher Filter)
ogr2ogr -f GPKG "%TEMP_RAW_GPKG%" "%INPUT_OSM%" ^
    -spat %BBOX% ^
    -skipfailures

IF NOT EXIST "%TEMP_RAW_GPKG%" (
    echo FEHLER: Export immer noch fehlgeschlagen. Das waere sehr ungewoehnlich.
    pause
    exit /b 1
)

REM 2. FILTERUNG & STRUKTURIERUNG
echo [2/3] Filtere Daten in saubere Layer...

REM A) Verkehrsnetz (Mit PROMOTE_TO_MULTI gegen die Warnungen)
echo    - Exportiere Verkehr...
ogr2ogr -f GPKG "%OUTPUT_GPKG%" "%TEMP_RAW_GPKG%" ^
    -nln "verkehrsnetz" ^
    -sql "SELECT geom, highway, surface, maxspeed, name, railway FROM lines WHERE highway IS NOT NULL OR railway IS NOT NULL" ^
    -nlt PROMOTE_TO_MULTI ^
    -overwrite

REM B) POIs
echo    - Exportiere POIs...
ogr2ogr -f GPKG "%OUTPUT_GPKG%" "%TEMP_RAW_GPKG%" ^
    -nln "poi_versorgung" ^
    -sql "SELECT geom, name, shop, amenity, highway FROM points WHERE shop IN ('supermarket', 'bakery', 'butcher', 'convenience') OR amenity IN ('doctors', 'pharmacy', 'school', 'kindergarten') OR highway = 'bus_stop'" ^
    -update

REM C) Flaechen
echo    - Exportiere Flaechen...
ogr2ogr -f GPKG "%OUTPUT_GPKG%" "%TEMP_RAW_GPKG%" ^
    -nln "landnutzung" ^
    -sql "SELECT geom, landuse, name FROM multipolygons WHERE landuse IN ('residential', 'industrial', 'commercial', 'retail')" ^
    -nlt PROMOTE_TO_MULTI ^
    -update

REM 3. CLEANUP
echo [3/3] Aufraeumen...
del "%TEMP_RAW_GPKG%"

echo.
echo --- FERTIG ---
echo Ergebnis: %OUTPUT_GPKG%
echo Hinweis: Die Karte ist nun rechteckig. In QGIS koennen Sie spaeter
echo einfach den VG250-Layer drueberlegen, um optisch zu begrenzen.
pause
exit /b 0

:hilfe
echo Aufruf: %~nx0 ^<OSM-Datei^> [Zielordner]
echo.
echo   OSM-Datei   Pfad zu einem OSM-Extrakt (.osm.pbf), der den Raum Aachen/Eifel
echo               abdeckt, z. B. ein Geofabrik-Download fuer NRW oder Deutschland.
echo   Zielordner  Ordner fuer das Ergebnis Simmerath_Analyse_Stabil.gpkg
echo               (Standard: Ordner dieses Skripts).
echo.
echo Beispiel: %~nx0 "D:\OSM\nordrhein-westfalen-latest.osm.pbf" "D:\Ergebnisse"
echo Voraussetzung: ogr2ogr (GDAL) im PATH, z. B. aus der OSGeo4W-Shell.
exit /b 2
