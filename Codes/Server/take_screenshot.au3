#Include <ScreenCapture.au3>

_Main()

Func _Main()

    Local $windowname = "SimCore IG"           ; Window name to capture
	;Local $windowname = "Untitled - Paint"    ; Window name to capture
    ;Local $images_save_path = "C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\images\"      ; File save path
	Local $images_save_path = ".\images\"      ; File save path
	Local $savename = "SimCore_screenshot"      ; Filename to save
    Local $overwrite = 1                        ; Bool: overwrite previous image?
    
    Local $trim_left = 10                        ; Trim pixels off from the screenshot
    Local $trim_up = 52
    Local $trim_right = 14
    Local $trim_down = 25
   
    DirCreate ( $images_save_path )
    
	$ws = WinGetClientSize($windowname)
	
	Local $name_number = 0
	Local $name = $images_save_path & $savename & ".png"
	if $overwrite = 0 then
		While FileExists($name)
			$name_number += 1
			$name = $images_save_path & $savename & "_" & $name_number & ".png"
		WEnd
	EndIf
	
	;_ScreenCapture_CaptureWnd($name, WinGetHandle($windowname), 0, 0, $ws[0]-$trim_left, $ws[1]-$trim_down, False)
	_ScreenCapture_CaptureWnd($name, WinGetHandle($windowname), $trim_left, $trim_up, $ws[0]-$trim_right, $ws[1]-$trim_down, False)
	
	;MsgBox(0,"image saved to", $images_save_path & $savename & ".png")
	
	
	Local $iW = ($ws[0] + 1 - $trim_left - $trim_right) / 2
	Local $iH = ($ws[1] + 1 - $trim_up - $trim_down) / 2
	;_ImageResize("C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\images\SimCore_screenshot.png", "C:\Program Files\Apache Software Foundation\Apache2.2\htdocs\images\SimCore_screenshot.jpg", $iW, $iH)
	;_ImageResize($name, $images_save_path & $savename & ".jpg", $iW, $iH)	
	
EndFunc
Func _ImageResize($sInImage, $sOutImage, $iW, $iH)
		Local $hWnd, $hDC, $hBMP, $hImage1, $hImage2, $hGraphic, $CLSID, $i = 0
		
		;OutFile path, to use later on.
		Local $sOP = StringLeft($sOutImage, StringInStr($sOutImage, "\", 0, -1))
		
		;OutFile name, to use later on.
		Local $sOF = StringMid($sOutImage, StringInStr($sOutImage, "\", 0, -1) + 1)
		
		;OutFile extension , to use for the encoder later on.
		Local $Ext = StringUpper(StringMid($sOutImage, StringInStr($sOutImage, ".", 0, -1) + 1))
		
		; Win api to create blank bitmap at the width and height to put your resized image on.
		$hWnd = _WinAPI_GetDesktopWindow()
		$hDC = _WinAPI_GetDC($hWnd)
		$hBMP = _WinAPI_CreateCompatibleBitmap($hDC, $iW, $iH)
		_WinAPI_ReleaseDC($hWnd, $hDC)
		
		;Start GDIPlus
		_GDIPlus_Startup()
		
		;Get the handle of blank bitmap you created above as an image
		$hImage1 = _GDIPlus_BitmapCreateFromHBITMAP ($hBMP)
		
		;Load the image you want to resize.
		$hImage2 = _GDIPlus_ImageLoadFromFile($sInImage)
		
		;Get the graphic context of the blank bitmap
		$hGraphic = _GDIPlus_ImageGetGraphicsContext ($hImage1)
		
		;Draw the loaded image onto the blank bitmap at the size you want
		_GDIPLus_GraphicsDrawImageRect($hGraphic, $hImage2, 0, 0, $iW, $iW)
		
		;Get the encoder of to save the resized image in the format you want.
		$CLSID = _GDIPlus_EncodersGetCLSID($Ext)
		
		;Generate a number for out file that doesn't already exist, so you don't overwrite an existing image.
		Do 
			$i += 1
		Until (Not FileExists($sOP & $i & "_" & $sOF))
		
		;Prefix the number to the begining of the output filename
		$sOutImage = $sOP & $i & "_" & $sOF
		
		;Save the new resized image.
		_GDIPlus_ImageSaveToFileEx($hImage1, $sOutImage, $CLSID)
		
		;Clean up and shutdown GDIPlus.
		_GDIPlus_ImageDispose($hImage1)
		_GDIPlus_ImageDispose($hImage2)
		_GDIPlus_GraphicsDispose ($hGraphic)
		_WinAPI_DeleteObject($hBMP)
		_GDIPlus_Shutdown()
	EndFunc

