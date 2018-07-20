for %%A in ("* *.txt") do call :sub "%%A"
goto :end

:sub
rem echo %1
set A=%1
ren %A% "%A: =%"

:end
rem pause