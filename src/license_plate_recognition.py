def recognize_plate(plate_region):
    import easyocr
    import cv2

    reader = easyocr.Reader(['en'], gpu=False)

    gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

    results = reader.readtext(thresh)
    print("[OCR DEBUG] Results:", results)  # 👈 add this

    if results:
        return results[0][1]
    else:
        return "UNKNOWN"
