
import math
from main_class import*
import pickle
import autopy
class position():  	
	def getLength(self,x1,y1,x2,y2):
		length= math.sqrt((x2-x1)**2+(y2-y1)**2)
		return length

	def getDirection(self,x1,y1,x2,y2,length,fingers):
		if length < 25 and self.Vars['idle']>0:
			print self.Vars['idle']
			if self.Vars['idle']>5:
				self.direction = self.fingerGesture(fingers)
			else:
				self.Vars['idle'] += 1		
		elif length>150 and x1+y1 !=0:
			self.Vars['idle'] = 0
			if(x2>x1):
				direction = "Right"
				print 'Right'
				# autopy.key.tap(autopy.key.K_RIGHT)
				autopy.key.type_string('n')
			else:
				direction = "Left "
				print 'Left'
				# call here event Left
				# autopy.key.tap(autopy.key.K_LEFT)
				autopy.key.type_string('p')
		else:
			direction = "None"
		pickle.dump(self.Vars, open(".config", "w"))		
		return direction

	def compute_position(self,current_x,current_y,frame,fingers):

		self.direction ="None" 
		try:
			self.Vars = pickle.load(open(".config", "r"))
			self.prev_x = self.Vars["prevX"]
			self.prev_y = self.Vars["prevY"]
			self.Vars["noCnt"] =0
		except:
			self.Vars["prevX"] =0
			self.Vars["prevY"] =0
		if (frame%10==0):
			self.Vars["prevX"] = current_x
			self.Vars["prevY"] = current_y
			self.current_x = current_x
			self.current_y = current_y
			pickle.dump(self.Vars, open(".config", "w"))
			# self.direction =[]
			length = self.getLength(self.prev_x,self.prev_y,self.current_x,self.current_y)
			self.direction = self.getDirection(self.prev_x,self.prev_y,self.current_x,self.current_y,length,fingers)			
			return self.direction
		else:
			return self.direction

	def fingerGesture(self,fingers):
		if fingers >3:				
			# autopy.key.tap('+', autopy.key.MOD_CONTROL)
			autopy.key.type_string (',')
			self.action = "Zoom IN"
			print 'zoom in'
			# zoom in
		# elif fingers ==3:
		# 	autopy.key.tap('0', autopy.key.MOD_CONTROL)
		# 	self.action = "Orig"
		# 	print 'Original'
		else:
			# autopy.key.tap(autopy.key.MOD_CONTROL)
			autopy.key.type_string ('.')
			self.action = "Zoom Out"
			print 'zoom out'
			# zoom Out
		return self.action
