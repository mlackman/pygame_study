import sys
import pygame
import math

class PositionAnimator:

  def __init__(self, total_time, target_position, attr_name, object):
    self.running = True
    self.total_time = total_time
    self.attr_name = attr_name
    self.object = object
    target_x, target_y = target_position
    self.attr_name = attr_name
    self.original_x, self.original_y = getattr(object, attr_name)
    self.dx = (target_x - self.original_x)
    self.dy = (target_y - self.original_y)
    self.start_time = None

  def animate(self, current_time):
    if self.running:
      if self.start_time == None:
        self.start_time = current_time
      duration = current_time - self.start_time
      dt = duration/self.total_time

      if dt > 1.0:
        dt = 1.0
        self.running = False

      value = -dt*(dt-2.0)

      x = self.original_x + self.dx * value
      y = self.original_y + self.dy * value

      setattr(self.object, self.attr_name, (x,y))
    


class World(object):

  def __init__(self):
    self._objects = []
    self._camera = None

  def add_object(self, game_object):
    self._objects.append(game_object)

  def set_camera(self, camera):
    self._camera = camera

  def render(self, surface):
    for obj in self._objects:
      self._render_object(obj, surface)

  def _render_object(self, graphic_object, surface):
    world_points = graphic_object.world_points
    camera_world_x, camera_world_y = self._camera.position
    # Move relative to camera position
    object_camera_points = [(x-camera_world_x, y-camera_world_y) for x,y in world_points]
    camera_width, camera_height = self._camera.size
    object_camera_points = [(x+camera_width/2.0, y+camera_height/2.0) for x,y in object_camera_points]

    surface_width = surface.get_width()
    surface_height = surface.get_height()

    aspect_ratio_width = surface_width / camera_width
    aspect_ratio_height = surface_height / camera_height

    # to screen coordinates
    graphic_object.screen_points = [(x*aspect_ratio_width, (camera_height-y)*aspect_ratio_height) for x,y in object_camera_points]
    graphic_object.render(surface)
    
    

class Camera(object):

  def __init__(self, position, size):
    self.size = size
    self.position = position


class Triangle(object):

  def __init__(self, position):
    self._points = [(0.0, 1.0), (1.0, -1.0), (-1.0, -1.0), (0.0, 1.0)] 
    self._points = [(x * 20, y*20) for x,y in self._points] # Scale
    self.position = position
    self.screen_points = None

  @property
  def world_points(self):
    pos_x, pos_y = self.position
    return [(pos_x + x, pos_y + y) for x,y in self._points]

  def render(self, surface):
    self.screen_points.append(self.screen_points[-1]) 
    for index, point in enumerate(self.screen_points[:-1]):
      pygame.draw.line(surface, (90, 50, 50), point, self.screen_points[index+1])
      
size = width, height = 640, 480
pygame.init()
screen = pygame.display.set_mode(size)

camera = Camera((100.0, 100.0), (640.0, 480.0))

world = World()
world.set_camera(camera)
triangle = Triangle((100.0, 100.0))
world.add_object(triangle)
surface = pygame.display.get_surface()

animator = PositionAnimator(2.5, (250.0, 250.0), "position", triangle)

clock = pygame.time.Clock()
while True:
  clock.tick(60)
  surface.fill( (0,0,0) )
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()

  current_time = pygame.time.get_ticks()/1000.0
  animator.animate(current_time)
  world.render(surface)  
  pygame.display.flip()
  