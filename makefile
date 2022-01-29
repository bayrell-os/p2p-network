
all:
	@echo "make {bdist|compile|clean}"

compile:
	pyinstaller -y -n p2p_network_1_0_linux ./run.py
	
bdist:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build/*
	rm -rf dist/*
	
