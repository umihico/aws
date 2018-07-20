Function load_metadata() As Variant
    Dim wb As Workbook, metadata_rows As Variant
    Set wb = Workbooks.Open("009_metadata_only_new.xlsx")
    load_metadata = wb.Worksheets(1).Cells(1, 1).CurrentRegion
    wb.Close False
End Function

Sub main()
    Workbooks.Open ("011_titletext_merged_rows.xlsx")
    Dim metadata As Variant, row As Long, company_name As String, company_code As String, doc_date As String, filepath As String
    metadata = load_metadata()
    For row = 1 To UBound(metadata, 1)
      Debug.Print (row)
      filepath = metadata(row, 1)
      company_name = metadata(row, 2)
      doc_date = metadata(row, 3)
      company_code = metadata(row, 4)
      Call convert_to_xlsx(filepath, company_name, doc_date, company_code)
    Next row
End Sub
Sub convert_to_xlsx(filepath, company_name, doc_date, company_code)
  Debug.Print (filepath)
  Dim wb As Workbook, image As Object, alt_text As String, title As String, text As String, image_address As Range, splited_inserting_text As Variant, text_row As Long
  Set wb = Workbooks.Open(filepath & "\merged.html")
  For Each image In wb.Worksheets(1).Shapes
    Set image_address = image.BottomRightCell
    Debug.Print (image_address.Address)
    alt_text = image.AlternativeText
    inserting_text = get_inserting_text(alt_text)
    splited_inserting_text = Split(inserting_text, vbLf)
    Rows(image_address.row + 1 & ":" & image_address.row + 1 + UBound(splited_inserting_text)).Insert Shift:=xlDown
    For text_row = 0 To UBound(splited_inserting_text)
      Cells(image_address.row + text_row, 1) = splited_inserting_text(text_row)
      Debug.Print (image_address.row + text_row & splited_inserting_text(text_row) & "end")
    Next text_row
    Rows(image_address.row & ":" & image_address.row + 1 + UBound(splited_inserting_text)).ClearFormats
    wb.Close True, company_code & "：" & company_name
  Next image


End Sub
Function get_inserting_text(alt_text) As String
  Dim wb As Workbook, ws As Worksheet, row_index As Long
  Set wb = Workbooks("011_titletext_merged_rows.xlsx")
  Set ws = wb.Worksheets(1)
  row_index = WorksheetFunction.Match(alt_text, ws.Columns(1), 0)
  title = ws.Cells(row_index, 2)
  text = ws.Cells(row_index, 3)
  get_inserting_text = "【IMAGE_TEXT_DETECTION】" & vbCrLf & title & vbCrLf & text & "【IMAGE_TEXT_DETECTION_END】"
  get_inserting_text = Replace(get_inserting_text, vbLf, vbCrLf)
  get_inserting_text = Replace(get_inserting_text, vbCr, vbCrLf)
  get_inserting_text = Replace(get_inserting_text, Chr(10) & Chr(10), Chr(10))
  get_inserting_text = Replace(get_inserting_text, Chr(10) & Chr(10), Chr(10))
  get_inserting_text = Replace(get_inserting_text, Chr(10) & Chr(10), Chr(10))
  get_inserting_text = Replace(get_inserting_text, Chr(10), vbCrLf)
'  Debug.Print (get_inserting_text)
'  Dim i As Long, l As String
'  For i = 1 To 100
'    l = Mid(get_inserting_text, i, 1)
'    Debug.Print (l)
'    Debug.Print (Asc(l))
'    Next i
'  Debug.Print (1 / 0)
End Function
