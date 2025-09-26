@echo off
echo.
echo === Installing Tesseract, Ghostscript, and ImageMagick ===
choco install tesseract-ocr -y
choco install ghostscript -y
choco install imagemagick.app -y
echo.

echo.
echo === Installing Python packages from requirements.txt ===
pip install -r requirements.txt
echo.

echo.
echo ###################################################
echo #                                                 #
echo #    ✅ Setup is Complete!                         #
echo #                                                 #
echo ###################################################
echo.
echo This window can now be closed.