#Handgunbubble_Animation
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
from kivy.graphics import Color, Rectangle, Ellipse, Rotate, PushMatrix, PopMatrix
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

#Needed for compiling exe with additional files per Kivy Docs
from kivy.resources import resource_add_path, resource_find

import os
import sys
import math
from random import randint


class BubbleWidget(Widget):
	def __init__(self, pos=(400,400), velocity=[1,0.1, 50],**kwargs):
		super(BubbleWidget, self).__init__(**kwargs)
		self.size_hint_x = None
		self.size_hint_y = None
		self.pos = pos
		self.size = (20,20)
		self.velocity = velocity
		self.maximum_size = velocity[2]
		blue = Color(0,0,1,1)
		self.bubble = Ellipse(size=self.size,pos=self.pos)
		self.canvas.add(blue)
		self.canvas.add(self.bubble)
		self.canvas.opacity = 0.7
		
		
		
		self.grown_bubble = False
	
		print('Bubble Velocity: ',self.velocity)
		
	
		self.bind(pos=self.redraw)
		self.bind(size=self.redraw)
		
		self.fps = 1/100
	
	def redraw(self, *args):
		self.bubble.size = self.size
		self.bubble.pos = self.pos
		
	def movement_v1(self, dt):
		step = 150
		scale = 1
		
		stepsize = step * scale * self.fps

		x = self.pos[0]+(stepsize * self.velocity[0])
		y = self.pos[1]+(stepsize * self.velocity[1])
		self.pos = (x,y)
		
		
	def on_parent(self, parent, widget):
		self.grow_clock = Clock.schedule_interval(self.growBubble, self.fps)
		
	
	def growBubble(self, dt):
		step = 150
		
		stepsize = step * self.fps

		if self.size[0]+stepsize < self.maximum_size:
			self.y -= stepsize/2
			self.x += stepsize/2
			diameter = stepsize+self.width
			
			self.size = (diameter,diameter)
		else:
			
			self.size = (self.maximum_size,self.maximum_size)
			self.grown_bubble = True
			self.grow_clock.cancel()
			
				
			if self.parent:
				self.parent.add_bubble()
			if self.x > Window.width:
				print("clock is still running for growbubble!")
			self.main_clock = Clock.schedule_interval(self.movement_v1, self.fps)
			
		
	
class HandImage(Image):
	def __init__(self, **kwargs):
		super(HandImage, self).__init__(*kwargs)
		
	
	def on_parent(self, parent, widget):
	
		self.source ='bubblewandtest.png'
		print('it happened')
		self.size_hint_x= None
		self.size_hint_y= None
		self.size=(150, 500)
		self.pos = (310, 80)
	
class MainLayout(FloatLayout):
	def __init__(self,**kwargs):
		super(MainLayout, self).__init__(**kwargs)
		self.size = (Window.width, Window.height)
		self.canvas.add(Color(1,1,1,1))
		self.bg = Rectangle(pos=self.pos, size=self.size)
		self.bubblewand = HandImage()
		
		self.canvas.add(self.bg)
		
		self.add_widget(self.bubblewand)
		
		
		main_fps = 1/60
		self.random_velocities = []
		max_x, min_x = 100, 80
		max_y, min_y = 40, -10
		min_size, max_size = 40, 75
		
		for i in range(20):
			rand_x = randint(min_x, max_x)
			rand_y = randint(min_y, max_y)
			rand_size = randint(min_size, max_size)

			rand_velocity = [rand_x/100, rand_y/100, rand_size]
			self.random_velocities.append(rand_velocity)
			print(i, '. ', rand_velocity)
			
		self.index = 19
		
		
		self.bind(height=self.redraw_background)
		self.bind(width=self.redraw_background)
		
		self.collision_clock = Clock.schedule_interval(self.check_boundries, main_fps)
		self.add_bubble()
		
	def add_bubble(self):
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
		
		
	def check_boundries(self, dt):
		for bubble in self.children[:]:
			if bubble.x > Window.width-200:
				self.remove_widget(bubble)
				print('deleted by main')		

class HandGunBubbleAnimationApp(App):
	def build(self):
		ml = MainLayout()
		return ml

if __name__ == '__main__':
	#necessary if compiling exe and adding files to --onefile option per Kivy docs
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))
		
	HandGunBubbleAnimationApp().run()