import xml.dom.minidom as md
import os

cov_file = md.parse("../tests/coverage.xml")
for y in cov_file.getElementsByTagName("package"):
    percentage = round(float(y.getAttribute("line-rate")),2)*100

os.system(f'cmd /k "set TEST_COVERAGE={percentage}"')
print(os.system('cmd /k "echo %TEST_COVERAGE%"'))
print(os.environ["TEST_COVERAGE"])

