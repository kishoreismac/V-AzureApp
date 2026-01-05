.PHONY: help test security clean format install

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run unit tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  security    - Run security checks"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean temporary files"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/unit/ -v

test-cov:
	python -m pytest tests/unit/ -v --cov=function_app --cov-report=term-missing

security:
	bandit -r function_app/ -f html -o bandit-report.html
	safety scan -r requirements.txt

format:
	black function_app/ tests/

clean:
	@echo "Cleaning temporary files..."
	@rmdir /s /q __pycache__ 2>nul || echo ""
	@rmdir /s /q function_app\__pycache__ 2>nul || echo ""
	@rmdir /s /q tests\__pycache__ 2>nul || echo ""
	@rmdir /s /q tests\unit\__pycache__ 2>nul || echo ""
	@del /q *.pyc 2>nul || echo ""
	@del /q function_app\*.pyc 2>nul || echo ""
	@del /q .coverage coverage.xml 2>nul || echo ""
	@echo "Cleanup complete!"