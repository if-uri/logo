.PHONY: site test deploy help
help:
	@grep -E "^[a-zA-Z_-]+:.*?## .*$$" $(MAKEFILE_LIST) | awk "BEGIN{FS=\":.*?## \"}{printf \"  %-10s %s\\n\",\$$1,\$$2}"
site: ## Build logo gallery _site/
	python3 scripts/build_site.py _site
test: ## Build the gallery and verify the output
	python3 scripts/build_site.py _site
	test -s _site/index.html
	grep -q ifuri-ecobar.js _site/index.html
deploy: ## Publish to logo.ifuri.com (Plesk)
	bash scripts/deploy-plesk.sh
