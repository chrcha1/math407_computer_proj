from mayavi import mlab
from tvtk.api import tvtk # python wrappers for the C++ vtk ecosystem
import numpy as np

def pack_rgb(r, g, b):
    rgb = (r<<16) + (g<<8) + b
    return rgb

def auto_sphere(image_file):
    img = tvtk.JPEGReader()
    img.file_name = "blue_marble_spherical.jpg"
    # map the texture
    texture = tvtk.Texture(input_connection=img.output_port, interpolate=0)

    # make the sphere
    R = 1
    Nrad = 180

    # create the sphere
    sphere = tvtk.TexturedSphereSource(radius=R, theta_resolution=Nrad,
                                       phi_resolution=Nrad)
    # assembly required
    sphere_mapper = tvtk.PolyDataMapper(input_connection=sphere.output_port)
    sphere_actor = tvtk.Actor(mapper=sphere_mapper, texture=texture)
    # plot
    mlab.clf()
    fig = mlab.figure(size=(800, 600), bgcolor=(1, 1, 1))
    fig.scene.add_actor(sphere_actor)

    for i in range(1):
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