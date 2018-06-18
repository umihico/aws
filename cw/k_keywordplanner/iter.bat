
cd /d %~dp0
for %%a in (raw_keyword_stat\*.csv) do (
  echo %%a
  copy "%%a" download.csv
  python_vba.bat
)
