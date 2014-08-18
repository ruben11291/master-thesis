
.PHONY: init
init: clean-test start-nodes clean-dist gen-dist change_cfg patch-dist start-processors

test: clean-test
	nosetests test/*.py

clean-test: 
	sh /tmp/DistributedSystem_grid/scripts/clean-test.sh
	
matrices: m/3C m/4C

m/%C: m/%A m/%B
	./src/plain-multiply.py $^ $@

m/3A:
	./src/gen-matrix.py $@ 1 50

m/3B:
	./src/gen-matrix.py $@ 2481 50

m/4A:
	./src/gen-matrix.py $@ 1 400

m/4B:
	./src/gen-matrix.py $@ 160001 400

################################### Makefile Distribuido #######################################

start-nodes:
	sh /tmp/DistributedSystem_grid/scripts/start-nodes.sh 
	
stop-nodes:
	sh /tmp/DistributedSystem_grid/scripts/stop-nodes.sh

start-processors:
	sh /tmp/DistributedSystem_grid/scripts/start-processors.sh 

patch-dist:
	sh /tmp/DistributedSystem_grid/scripts/patch-dist.sh
	
gen-dist: 
	sh /tmp/DistributedSystem_grid/scripts/gen-dist.sh

change_cfg:
	sh /tmp/DistributedSystem_grid/scripts/change_cfg.sh

client:
	sh /tmp/DistributedSystem_grid/scripts/client.sh

clean-dist:
	sh /tmp/DistributedSystem_grid/scripts/clean-dist.sh