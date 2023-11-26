#Rokcet Animation
#@Michael Brown: BubbleCipherStudios

from kivy.config import Config

DisplayWidth = 1080
DisplayHeight = 720

Dimensions = (DisplayWidth, DisplayHeight)

Config.set('graphics', 'width', DisplayWidth)
Config.set('graphics', 'height', DisplayHeight)

Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.button import Button
from kivy.core.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

#Needed for compiling exe with additional files per Kivy Docs
from kivy.resources import resource_add_path, resource_find

import os
import sys
import math
from random import randint

### TODO LIST ###
'''
-Create Bubbles class
	will have same circle canvas
	will have random size eg 5-20
	will have random velocity
	will have a calculated maximum offset (for wavy movement)
	will have constant x velocity, changing y velocity
	will have a collision check for the boundry on rightside
'''

class BubbleWidget(Widget):
	def __init__(self, pos=(300,300), maximum_size=(50,50), velocity=[1,0.1],**kwargs):
		super(BubbleWidget, self).__init__(**kwargs)
		self.size_hint_x = None
		self.size_hint_y = None
		self.pos = pos
		self.size = (10,10)
		self.maximum_size = maximum_size
		blue = Color(0,0,1,1)
		self.bubble = Ellipse(size=(10,10),pos=self.pos)
		self.canvas.add(blue)
		self.canvas.add(self.bubble)
		self.canvas.opacity = 0.5
		
		
		self.velocity = velocity
		self.going_up = False
		self.y_up = 50
		self.y_down = self.y_up/3
		self.y_remaining = self.y_up
	
		self.bind(pos=self.redraw)
		self.bind(size=self.redraw)
		
		self.fps = 1/60
	
	def redraw(self, *args):
		self.bubble.size = self.size
		self.bubble.pos = self.pos
		
	def movement_v1(self, dt):
		step = 100
		scale = 1
		vel_increment = 0.001
		
		stepsize = step * scale * self.fps

		x = self.pos[0]+(stepsize * self.velocity[0])
		y = self.pos[1]+(stepsize * self.velocity[1])
		self.pos = (x,y)
		
		if self.parent and x > Window.width-200:
			self.parent.remove_widget(self)


	def movement_x(self, dt):
		step = 100
		scale = 1
		
		stepsize = step * scale * self.fps

		self.x += (stepsize * self.velocity[0])
		
		if self.parent and self.x > Window.width:
			self.parent.remove_widget(self)


### FIX ME ### Currently snapping to max y pos when done with growing bubble
	def movement_y(self, dt):

		if self.going_up:
			if self.y_remaining >= 0:
				step = (self.y_remaining ** 2) * self.velocity[1] * (self.fps)
				
				if self.y_remaining < 0:
					step *= -1

				self.y_remaining -= step
				self.y += step
			# else:
				# self.going_up = False
				# if self.y_remaining <= self.down:
					# step = (self.y_remaining ** 2) * scale * self.fps
				
				# if self.y_remaining < 0:
					# step *= -1

				# self.y_remaining -= 1
				# self.y += step
			
		
		if self.parent and self.y > Window.height:
			self.parent.remove_widget(self)

	def on_parent(self, parent, widget):
		self.movementx_clock = Clock.schedule_interval(self.movement_x, self.fps)
		self.movementy_clock = Clock.schedule_interval(self.movement_y, self.fps)
		self.grow_clock = Clock.schedule_interval(self.grow_bubble, self.fps)
		
	
	def grow_bubble(self, dt):
		step = 200
		scale = 1
		stepsize = step * self.fps

		if self.size[0] < self.maximum_size[0]:
			diameter = stepsize+self.width
			self.size = (diameter, diameter)
		else:
			self.going_up = True
			self.grow_clock.cancel()
		
		
class HandImage(Image):
	pass
	
class MainLayout(FloatLayout):
	def __init__V1(self,**kwargs):
		super(MainLayout, self).__init__(**kwargs)
		self.size = (Window.width, Window.height)
		self.canvas.add(Color(1,1,1,1))
		self.bg = Rectangle(pos=self.pos, size=self.size)
		self.canvas.add(self.bg)
		
		self.random_velocities = []
		max_x, min_x = 150, 100
		max_y, min_y = 100, 0
		
		for i in range(20):
			rand_x = randint(min_x, max_x)
			rand_y = randint(min_y, max_y)
			rand_velocity = [rand_x/100, rand_y/100]
			self.random_velocities.append(rand_velocity)
			print(i, '. ', rand_velocity)
			
		self.index = 19
		
		
		self.bind(height=self.redraw_background)
		self.bind(width=self.redraw_background)
		
		Clock.schedule_interval(self.add_bubble, 1/5)
		
	def __init__(self,**kwargs):
		super(MainLayout, self).__init__(**kwargs)
		self.size = (Window.width, Window.height)
		self.canvas.add(Color(1,1,1,1))
		self.bg = Rectangle(pos=self.pos, size=self.size)
		self.canvas.add(self.bg)
		
		self.random_velocities = []
		max_x, min_x = 150, 100
		max_y, min_y = 100, 0
		
		for i in range(20):
			rand_x = randint(min_x, max_x)
			rand_y = randint(min_y, max_y)
			rand_velocity = [rand_x/100, rand_y/100]
			self.random_velocities.append(rand_velocity)
			print(i, '. ', rand_velocity)
			
		self.index = 19
		
		
		self.bind(height=self.redraw_background)
		self.bind(width=self.redraw_background)
		
		Clock.schedule_interval(self.add_bubble, 1/5)
		
	def add_bubble(self, dt):
		if self.index > 0:
			rand_vel = self.random_velocities[self.index]
			self.index -= 1
		else:
			rand_vel = self.random_velocities[self.index]
			self.index = 19
		
		
		self.add_widget(BubbleWidget(velocity=rand_vel))
	
	def redraw_background(self, *args):
		self.bg.size = (self.width,self.height)
		self.bg.pos = self.pos


class HandGunBubbleAnimationApp(App):
	def build(self):
		ml = MainLayout()
		return ml

if __name__ == '__main__':
	#necessary if compiling exe and adding files to --onefile option per Kivy docs
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))
		
	HandGunBubbleAnimationApp().run()
