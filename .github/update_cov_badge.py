import xml.dom.minidom as md

cov_file = md.parse("../coverage.xml")
for y in cov_file.getElementsByTagName("package"):
    percentage = round(float(y.getAttribute("line-rate")), 2)*100

print(percentage)

