from mayavi import mlab
from tvtk.api import tvtk # python wrappers for the C++ vtk ecosystem
import numpy as np

def pack_rgb(r, g, b):
    rgb = (r<<16) + (g<<8) + b
    return rgb

def auto_sphere(image_file):
    # create a figure window (and scene)
    fig = mlab.figure(size=(600, 600))

    # load and map the texture
    # img = tvtk.JPEGReader()
    # img.file_name = image_file
    # texture = tvtk.Texture(input_connection=img.output_port, interpolate=1)
    # (interpolate for a less raster appearance when zoomed in)

    # use a TexturedSphereSource, a.k.a. getting our hands dirty
    R = 1
    Nrad = 180

    # create the sphere source with a given radius and angular resolution
    sphere = tvtk.TexturedSphereSource(radius=R, theta_resolution=Nrad,
                                       phi_resolution=Nrad)

    # assemble rest of the pipeline, assign texture
    sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
    sphere_actor = tvtk.Actor(mapper=sphere_mapper)
    fig.scene.add_actor(sphere_actor)

    K = 20
    xx = np.arange(0, K, 1)
    yy = np.arange(0, K, 1)

    x, y = np.meshgrid(xx, yy)
    x, y = x.flatten(), y.flatten()
    z = np.zeros(K * K)

    nodes = mlab.points3d(x, y, z, scale_factor=0.05)
    nodes.glyph.scale_mode = 'scale_by_vector'
    for i in range(1000):
        x,y,z = sample_spherical(1)
        sx, sy, sz = .05,.05,.05
        colors = [pack_rgb(0, 255, 0) for _ in range(10)]
        pts = mlab.quiver3d(x, y, z, sx, sy, sz, scalars=1, mode="sphere", scale_factor=.25)
        pts.glyph.scale_mode = 'scale_by_vector'
        pts.mlab_source.dataset.point_data.scalars = colors
        #pts.glyph.color_mode = "color_by_scalar"
        pts.glyph.glyph_source.glyph_source.center = [0, 0, 0]


def sample_spherical(npoints, ndim=3):
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    return vec

if __name__ == "__main__":
    image_file = 'blue_marble_spherical.jpg'
    auto_sphere(image_file)
    print(sample_spherical(4,4))
    mlab.show()