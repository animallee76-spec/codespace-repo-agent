
    SHELL := /bin/bash
    .PHONY: doctor dry run

    doctor:
	python -m agent.main doctor

    dry:
	python -m agent.main run --dry

    run:
	python -m agent.main run
