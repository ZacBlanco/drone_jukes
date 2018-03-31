#! /usr/bin/bash

make -j8

gcc -pthread -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I/home/zac/projects/drone_jukes/pyyolo/env/lib/python3.5/site-packages/numpy/core/include -I/home/common/darknet3/include -I/home/common/darknet3/src -I/usr/include/python3.5m -I/home/zac/projects/drone_jukes/pyyolo/env/include/python3.5m -c module.c -o build/temp.linux-x86_64-3.5/module.o
gcc -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 build/temp.linux-x86_64-3.5/module.o -L. -L/usr/local/cuda/lib64 -L/usr/local/ -lyolo -lcuda -lcudart -lcublas -lcurand -lcudnn -o build/lib.linux-x86_64-3.5/pyyolo.cpython-35m-x86_64-linux-gnu.so

python setup_gpu.py install

python pyyolo_test.py