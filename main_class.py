from convexHull import*
import numpy as np
import cv2
import pickle, time, os, threading
import common
import pickle
class startTracing():
  def __init__(self,video_src):
		self.direction = "None"
		self.debugMode = True
		self.fingers = 0
		self.frame = 0
		self.camera = cv2.VideoCapture(video_src)
		self.camera.set(3,640)
		self.camera.set(4,480)
		
		self.posPre = 0  
		self.Data = {"angles less 90" : 0,
					 "cursor" : (0, 0),
					 "hulls" : 0, 
					 "defects" : 0,
					 "fingers": 0,
					 "fingers history": [0],
					 "area": 0,
					 }

		self.lastData = self.Data

		try:  
			self.Vars = pickle.load(open(".config", "r"))
			self.Vars['idle'] = 0
			pickle.dump(self.Vars, open(".config", "w"))

		except:
			print "Config file not found."
			exit()

		cv2.namedWindow("Filters")
		cv2.createTrackbar("erode", "Filters", self.Vars["erode"], 255, self.erode)
		cv2.createTrackbar("dilate", "Filters", self.Vars["dilate"], 255, self.dilate)
		cv2.createTrackbar("smooth", "Filters", self.Vars["smooth"], 255, self.smooth)
		cv2.createTrackbar("upper", "Filters", self.Vars["upper"], 255, self.onChange_upper)
		cv2.createTrackbar("lower", "Filters", self.Vars["lower"], 255, self.onChange_lower)
	#----------------------------------------------------------------------
	def erode(self, value):
		self.Vars["erode"] = value + 1
		pickle.dump(self.Vars, open(".config", "w"))
		
	#----------------------------------------------------------------------
	def dilate(self, value):
		self.Vars["dilate"] = value + 1
		pickle.dump(self.Vars, open(".config", "w"))
		
	#----------------------------------------------------------------------
	def smooth(self, value):
		self.Vars["smooth"] = value + 1
		pickle.dump(self.Vars, open(".config", "w"))
			
	#----------------------------------------------------------------------
	def onChange_upper(self, value):
		self.Vars["upper"] = value
		pickle.dump(self.Vars, open(".config", "w"))
		
	#----------------------------------------------------------------------
	def onChange_lower(self, value):
		self.Vars["lower"] = value
		pickle.dump(self.Vars, open(".config", "w"))

	#-----------------------------------------------------------------------
	def filterSkin(self, im):
		"""Aplica el filtro de piel."""
		UPPER = np.array([self.Vars["upper"], self.Vars["filterUpS"], self.Vars["filterUpV"]], np.uint8)
		LOWER = np.array([self.Vars["lower"], self.Vars["filterDownS"], self.Vars["filterDownV"]], np.uint8)
		hsv_im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
		filter_im = cv2.inRange(hsv_im, LOWER, UPPER)
		return filter_im
	#-----------------------------------------------------------------------
	def run(self):
		while True:
			if (self.frame%10 == 0):
				self.frame = 1
			else:
				self.frame = self.frame +1
			ret, im = self.camera.read()
			im = cv2.flip(im, 1)
			self.imOrig = im.copy()
			self.imNoFilters = im.copy()
			im = cv2.blur(im, (self.Vars["smooth"], self.Vars["smooth"]))
			filter_ = self.filterSkin(im)
			filter_ = cv2.erode(filter_,
								cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(self.Vars["erode"], self.Vars["erode"])))           
			
			filter_ = cv2.dilate(filter_,
								 cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(self.Vars["dilate"], self.Vars["dilate"])))
			dilated = filter_.copy()
			cv2.imshow('dilated',dilated)
			try:
				vis,self.fingers, self.direction=findConvexHull().drawConvex(filter_,self.imOrig,self.frame)			
			except:
				# dilated = self.imOrig
				vis = self.imOrig
			common.draw_str(vis, (20, 50), 'No of fingers: ' + str(self.fingers))
			common.draw_str(vis, (20, 80), 'Movement of contour:' + str(self.direction))		
			cv2.imshow('image',vis)
			if cv2.waitKey(1) == 27:
				break
#-----------------------------------------------------------------------
if __name__ == '__main__':
	import sys
	try: video_src = sys.argv[1]
	except: video_src = 0
	startTracing(video_src).run()
