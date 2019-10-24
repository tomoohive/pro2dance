docker build -t pro2dance:latest .

cd ..

docker run --rm -v  $PWD:/pro2dance/ -it pro2dance:latest /bin/bash -c "cd pro2dance/tf-pose-estimation/tf_pose/pafprocess && swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace && cd / && /bin/bash"
