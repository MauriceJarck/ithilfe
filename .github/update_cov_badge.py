import xml.dom.minidom as md
import os

cov_file = md.parse("../tests/coverage.xml")
for y in cov_file.getElementsByTagName("package"):
    percentage = round(float(y.getAttribute("line-rate")),2)*100
print(os.environ["TEST_COVERAGE "])

os.environ["TEST_COVERAGE "] = str(percentage)

print(os.environ["TEST_COVERAGE "])

