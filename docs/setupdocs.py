from docs import conf
# conf file
conf.extensions.append('sphinx.ext.napoleon')
conf.html_theme = "sphinx_rdt_theme"
print(conf.extensions)
print(conf.html_theme)