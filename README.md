# Ringbuffer for n-dimensional data based on numpy
This is a simple implementation for a ringbuffer for n-dimensional data. The implementation allows for multiple read indeces, e.g. for multiple processes reading the same data. In the current implementation an exception is raised if a process tries to overwrite data that has not been read.

## Examples
```python

# EXAMPLES

# new buffer
print('One dimensional ring buffer')
ring = Ringbuffer((20))

# writing data
print('writing ...')
ring.write(np.random.random((4)))
print(ring.buffer.T)
print('\n')
ring.write(np.random.random((16)))
print(ring.buffer.T)

# reading data
print('\nreading ...')
print(ring.read(4).T)
print('\n')
print(ring.read().T)
print('\nsecond read index')
ring.set_new_read_index('no2')
print(ring.read(4, inx_name='no2').T)
print('\n')
print(ring.read(inx_name='no2').T)
```
```
One dimensional ring buffer
writing ...
[ 0.25201103  0.82238187  0.96519156  0.8906403   0.          0.          0.
  0.          0.          0.          0.          0.          0.          0.
  0.          0.          0.          0.          0.          0.        ]


[ 0.25201103  0.82238187  0.96519156  0.8906403   0.72460653  0.44403199
  0.20520901  0.87100261  0.9441303   0.09061483  0.25843096  0.43792633
  0.65519508  0.74939183  0.94901315  0.07786692  0.97516227  0.46809906
  0.44071932  0.48524725]

reading ...
[ 0.25201103  0.82238187  0.96519156  0.8906403 ]


[ 0.72460653  0.44403199  0.20520901  0.87100261  0.9441303   0.09061483
  0.25843096  0.43792633  0.65519508  0.74939183  0.94901315  0.07786692
  0.97516227  0.46809906  0.44071932  0.48524725]

second read index
[ 0.25201103  0.82238187  0.96519156  0.8906403 ]


[ 0.72460653  0.44403199  0.20520901  0.87100261  0.9441303   0.09061483
  0.25843096  0.43792633  0.65519508  0.74939183  0.94901315  0.07786692
  0.97516227  0.46809906  0.44071932  0.48524725]
```
``` python
# new buffer
print('3 dimensional ring buffer')
ring = Ringbuffer((6, 2, 2))

# writing data
print('writing ...')
ring.write(np.random.random((1,2,2)))
print(ring.buffer.T)
print('\n')
ring.write(np.random.random((5,2,2)))
print(ring.buffer.T)

# reading data
print('\nreading ...')
print(ring.read(1).T)
print('\n')
print(ring.read().T)
```

```
3 dimensional ring buffer
writing ...
[[[ 0.35968431  0.          0.          0.          0.          0.        ]
  [ 0.74806535  0.          0.          0.          0.          0.        ]]

 [[ 0.04795518  0.          0.          0.          0.          0.        ]
  [ 0.94318894  0.          0.          0.          0.          0.        ]]]


[[[ 0.35968431  0.79421716  0.11040488  0.14039704  0.24449649  0.36381339]
  [ 0.74806535  0.7604594   0.36582424  0.06743808  0.89862781  0.66174326]]

 [[ 0.04795518  0.50828856  0.71369883  0.68972996  0.66897394  0.87398903]
  [ 0.94318894  0.07989122  0.40706933  0.46006208  0.94027497  0.91696824]]]

reading ...
[[[ 0.35968431]
  [ 0.74806535]]

 [[ 0.04795518]
  [ 0.94318894]]]


[[[ 0.79421716  0.11040488  0.14039704  0.24449649  0.36381339]
  [ 0.7604594   0.36582424  0.06743808  0.89862781  0.66174326]]

 [[ 0.50828856  0.71369883  0.68972996  0.66897394  0.87398903]
  [ 0.07989122  0.40706933  0.46006208  0.94027497  0.91696824]]]
```
