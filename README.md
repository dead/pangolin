# pangolin

The project implements a python binding for 3D visualization library **[Pangolin](http://github.com/stevenlovegrove/Pangolin)**.

> Pangolin is a lightweight portable rapid development library for managing OpenGL
display / interaction and abstracting video input. At its heart is a simple
OpenGL viewport manager which can help to modularise 3D visualisation without
adding to its complexity, and offers an advanced but intuitive 3D navigation
handler. Pangolin also provides a mechanism for manipulating program variables
through config files and ui integration, and has a flexible real-time plotter
for visualising graphical data.  
The ethos of Pangolin is to reduce the boilerplate code that normally
gets written to visualise and interact with (typically image and 3D
based) systems, without compromising performance. It also enables write-once
code for a number of platforms, currently including Windows, Linux, OSX, Android
and IOS.

This binding is primarily written for SLAM related visualization in python, for convenience, I write some handy functions 
(DrawPoints, DrawLines, DrawCameras, DrawBoxes) for drawing point clouds, trajectory, poses and 3d bounding boxes. These functions can access numpy array directly, so are very efficient. Actually, this library has little python overload.  
Some of Pangolin's C++ functions are not wrapped, for implemented part, see [examples](python/examples)
or [Gallery](#Gallery) below.  


## Requirements
* C++: [dependencies](#Dependencies).   
This project also relies on [pybind11](https://github.com/pybind/pybind11), 
but it's built in this repository, you don't need to install.  
* Python: To run those python examples, 
you should have [numpy](http://www.numpy.org/) and [PyOpenGL](http://pyopengl.sourceforge.net/) installed. 


## Installation
```
git clone https://github.com/uoip/pangolin.git
cd pangolin
mkdir build
cd build
cmake ..
make -j8
cd ..
python setup.py install
```
Tested under Ubuntu 16.04, Python 3.6+.

## Getting started
The code below create a window, and render a cube and a cloud of points.
```python
import numpy as np
import OpenGL.GL as gl
import pangolinpy as pangolin

pangolin.CreateWindowAndBind('Main', 640, 480)
gl.glEnable(gl.GL_DEPTH_TEST)

# Define Projection and initial ModelView matrix
scam = pangolin.OpenGlRenderState(
    pangolin.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 100),
    pangolin.ModelViewLookAt(-2, 2, -2, 0, 0, 0, pangolin.AxisDirection.AxisY))
handler = pangolin.Handler3D(scam)

# Create Interactive View in window
dcam = pangolin.CreateDisplay()
dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0/480.0)
dcam.SetHandler(handler)

while not pangolin.ShouldQuit():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(1.0, 1.0, 1.0, 1.0)
    dcam.Activate(scam)
    
    # Render OpenGL Cube
    pangolin.glDrawColouredCube()

    # Draw Point Cloud
    points = np.random.random((100000, 3)) * 10
    gl.glPointSize(2)
    gl.glColor3f(1.0, 0.0, 0.0)
    pangolin.DrawPoints(points)

    pangolin.FinishFrame()

```
As shown above, this library works seamlessly with PyOpenGL and numpy, it can access 
numpy array directly without copying data (thanks to [pybind11](https://github.com/pybind/pybind11)).  

## <a name="Gallery">Gallery</a>
**[HelloPangolin.py](python/examples/HelloPangolin.py)** (point cloud and 3d object):  
![](python/examples/imgs/HelloPangolinColorful.png)

**[SimpleDisplayImage.py](python/examples/SimpleDisplayImage.py)** (image and 3d object):  
![](python/examples/imgs/SimpleDisplayImage.png)
 
**[SimpleDisplayMenu.py](python/examples/SimpleDisplayMenu.py)** (basic GUI):  
![](python/examples/imgs/SimpleDisplayMenu.png)

**[SimpleMultiDisplay.py](python/examples/SimpleMultiDisplay.py)** (multiple display windows):  
![](python/examples/imgs/SimpleMultiDisplay.png)

**[SimplePlot.py](python/examples/SimplePlot.py)** (2d plot):  
![](python/examples/imgs/SimplePlot.png)

**[SimplePlotDisplay.py](python/examples/SimplePlotDisplay.py)** (2d plot and 3d object):  
![](python/examples/imgs/SimplePlotDisplay.png)

**[simple_draw.py](python/examples/simple_draw.py)** draw point clouds, camera/pose, 3d boxes, lines(consecutive or separate):  
![](python/examples/imgs/simple_draw.png)

## License
Follow **[Pangolin](http://github.com/stevenlovegrove/Pangolin)**, the C++ binding code and 
python example code of this project is released under MIT License.

## Contact
If you have problems related to **binding code/python interface/python examples** of this project, 
you can report isseus, or email me (qihang@outlook.com).
