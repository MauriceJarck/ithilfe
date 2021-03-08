import xml.dom.minidom as md

cov_file = md.parse("../tests/coverage.xml")
for y in cov_file.getElementsByTagName("package"):
    percentage = round(float(y.getAttribute("line-rate")),2)*100

badge_file = md.parse("cov_badge.svg")
for x in badge_file.getElementsByTagName("text"):
    if str(x.firstChild.nodeValue).endswith("%"):
        old = x.firstChild.nodeValue
        x.firstChild.nodeValue = str(percentage)+"%"
        new = x.firstChild.nodeValue
        if old != new:
            print(f"old: {old}, new: {new}")

with open("../.github/cov_badge.svg", "w") as fs:
    fs.write(badge_file.toxml())
    fs.close()