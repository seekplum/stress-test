define PRINT_HELP_PYSCRIPT
import re, sys

print("make option")
print("  --option:")
for line in sys.stdin:
    match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("    {:<20}{}".format(target, help))
endef
export PRINT_HELP_PYSCRIPT

define rm_container
    docker stop $(1) >/dev/null 2>&1; echo "stop $(1)"
    docker rm $(1) >/dev/null 2>&1; echo "remove $(1)"
endef

BROWSER := python -c "$$BROWSER_PYSCRIPT"
WORK_DIRECTORY := /tmp/prometheus

# Makefile中的第一个目标会被作为其默认目标
help: ## 帮助信息
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# 声明伪目标
.PHONY: clean

py-format: # 格式化 Python 代码
	@autoflake -r --in-place --remove-unused-variables --ignore-init-module-imports fastapi-stress flask-stress sanic-stress tornado-stress  ## 移除无用import
	@isort -rc --atomic fastapi-stress flask-stress sanic-stress tornado-stress  ## 排序import
	@black --line-length=120 --target-version=py27 fastapi-stress flask-stress sanic-stress tornado-stress  ## 格式化代码

clean: ## 清除无效文件
	@rm -rf build dist
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name 'htmlcov' -exec rm -rf {} +
	@find . -name '.coverage*' -exec rm -rf {} +
	@find . -name '.pytest_cache' -exec rm -rf {} +
	@find . -name '.benchmarks' -exec rm -rf {} +
	@find . -name '*.egg-info' -exec rm -rf {} +
