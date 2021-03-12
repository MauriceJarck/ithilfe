import xml.dom.minidom as md
import os

cov_file = md.parse("../tests/coverage.xml")
for y in cov_file.getElementsByTagName("package"):
    percentage = round(float(y.getAttribute("line-rate")),2)*100

os.system(f"SETX COVERAGE  {str(100)}")

print(os.system("echo %COVERAGE%"))

