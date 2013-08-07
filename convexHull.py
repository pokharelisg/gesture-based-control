from position import*
import cv2
import numpy as np
import os
import math
import pickle
class findConvexHull():
  def __init__(self):
		self.long_contour = []
	def getLength(self,orgn_x,orgn_y,x1,y1,x2,y2):
		l2= math.sqrt((x2-orgn_x)**2+(y2-orgn_y)**2)
		l1= math.sqrt((x1-orgn_x)**2+(y1-orgn_y)**2)
		if l2>l1:
			return l2
		else:
			return l1
	#----------------------------------------------------------------------------------
	def getLongestContour(self,contours):
		prev_cntLength=0
		# longestCnt = [0]
		for cnt in contours:
			Area = cv2.contourArea(cnt)
			if Area > 4000:
				try:
					prev_length = 0					
					hull = cv2.convexHull(cnt,returnPoints = False)
					# approx = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)
					defects = cv2.convexityDefects(cnt,hull)
					s,e,f,d = defects[0,0]
					start = tuple(cnt[s][0])
					end = tuple(cnt[e][0])
					orgn_x = start[0]
					orgn_y = start[1]
					try:
						for i in range(1,defects.shape[0]):
							s,e,f,d = defects[i,0]
							start = tuple(cnt[s][0])
							end = tuple(cnt[e][0])
							far = tuple(cnt[f][0])
							x1 = start[0]
							y1 = start[1]
							x2 =end[0]
							y2 = end[1]

							length =findConvexHull().getLength(orgn_x,orgn_y,x1,y1,x2,y2)
							if length > prev_length:
								prev_length = length
						cntLength = prev_length
						if cntLength > prev_cntLength:
							longestCnt = cnt
					except:
						prev_length = 0
				except:
					prev_length = 0			
		return longestCnt, cntLength
	#----------------------------------------------------------------------------------
	def drawConvex(self,dilated,img,frame):
		self.Area = 0		
		self.fingers = -1
		depth =0
		contours, hier = cv2.findContours(dilated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		
		if len(contours) == 0: return

		longestCnt, cntLength = findConvexHull().getLongestContour(contours)
		# cv2.drawContours(img,contours,0,(0,255,0),2)
		if cntLength >220:
			try:
				hull = cv2.convexHull(longestCnt,returnPoints = False)
				approx = cv2.approxPolyDP(longestCnt,0.05*cv2.arcLength(longestCnt,True),True)
				defects = cv2.convexityDefects(longestCnt,hull)
				try:
					palm_bound_x = []
					palm_bound_y = []
					for i in range(defects.shape[0]):
						s,e,f,d = defects[i,0]
						start = tuple(longestCnt[s][0])
						end = tuple(longestCnt[e][0])
						far = tuple(longestCnt[f][0])

						x1 = start[0]
						y1 = start[1]
						x2 =end[0]
						y2 = end[1]
						x3 = far[0]
						y3 = far[1]
						cv2.line(img,start,end,[255,0,0],2)
						if d >5000:
							palm_bound_x.append(x3)
							palm_bound_y.append(y3)
							cv2.circle(img,far,3,[0,0,255],-1)						
							self.fingers = self.fingers+1
						else:
							cv2.circle(img,far,3,[0,255,255],-1)
					# print palm_bound_x, palm_bound_y
				except:
					print 'no shapes'
					approx = 0
			except:
				print 'no longestCnt shapes'
			M = cv2.moments(longestCnt)
			centroid_x = int(M['m10']/M['m00'])
			centroid_y = int(M['m01']/M['m00'])				
			cv2.circle(img, (centroid_x, centroid_y), 7, (100,255,100), -1)
			# self.direction = position().compute_position(centroid_x,centroid_y,frame)
		else:
			self.Vars = pickle.load(open(".config", "r"))
			if(frame%10==0 and self.Vars["noCnt"]>3):
				# print self.Vars['noCnt']
				self.Vars["noCnt"] =0
				self.Vars["prevX"] =0
				self.Vars["prevY"] =0
				self.Vars['idle'] = 1
 				self.direction = "None"
 				pickle.dump(self.Vars, open(".config", "w"))
			else:
				self.Vars["noCnt"] +=1
				# print 'a=',self.Vars['noCnt']
				self.direction = "None"
			pickle.dump(self.Vars, open(".config", "w"))
		if self.fingers>=0:
			self.fingers = self.fingers
		else:
			self.fingers =0
		self.Vars = pickle.load(open(".config", "r"))
		self.direction = position().compute_position(centroid_x,centroid_y,frame,self.fingers)
		return img,self.fingers, self.direction

#------------------------------------------------------------------------------------------------
