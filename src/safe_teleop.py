#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist
class avoider():
	def __init__(self):
		self.dist_max=95.0
		self.dist_min1=33.0
		self.dist_min2=41.0
		self.vit1=0.001
		self.vit2=0.002
		self.vit3=0.003
		self.boucle1=False
		self.boucle2=False
		self.boucle3=False
		self.boucle4=False
		self.boucle5=False
		self.boucle6=False
		self.end=False
		self.count = 0
		self.t=0.0
		self.twist=Twist()
		self.az=self.lx=self.s1=self.s2=self.s3=self.s4=self.s5=self.r1=self.r2=self.r3=self.r4=self.r5=0.0
		rospy.Subscriber('cmd_vel_in', Twist,self.callback)
		rospy.Subscriber("US1", Range, self.us1)
		rospy.Subscriber("US2",Range, self.us2)
		rospy.Subscriber("US3", Range, self.us3)
		rospy.Subscriber("US4", Range, self.us4)
		rospy.Subscriber("US5", Range, self.us5)
		rospy.Subscriber("IR1", Range, self.ir1)
		rospy.Subscriber("IR2", Range, self.ir2)
		rospy.Subscriber("IR3", Range, self.ir3)
		rospy.Subscriber("IR4", Range, self.ir4)
		rospy.Subscriber("IR5", Range, self.ir5)
		self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
	def control(self):
		tmp=self.r5
		self.r5=self.r1
		self.r1=tmp
		tmp=self.r2
		self.r2=self.r4
		self.r4=tmp
		if self.s1>35.0:
			v1=self.s1
		else:
			v1=self.r1
		if self.s2>35.0:
			v2=self.s2
		else:
			v2=self.r2
		#if s3>35.0:
		#v3=s3
		#else:
		v3=self.r3
		if self.s4>35.0:
			v4=self.s4
		else:
			v4=self.r4
		if self.s5>35.0:
			v5=self.s5
		else:
			v5=self.r5
		self.lx=self.twist.linear.x
		self.az=self.twist.angular.z
		rospy.loginfo("v1=%s v2=%s v3=%s v4=%s v5=%s ",v1,v2,v3,v4,v5)
		if self.lx>0:
			if v1<=self.dist_min2 or v2<=self.dist_min1 or v3<=self.dist_min1 or v4<=self.dist_min1 or v5<=self.dist_min2:
				self.lx=0
				self.az=0
			elif (v1<self.dist_max  or v2<self.dist_max)  and v3<self.dist_max and v4 >self.dist_max and v5>self.dist_max and v1 >self.dist_min2 and v2>self.dist_min1 and v3>self.dist_min1:
				self.lx=self.vit1
				self.az=-1.0
				self.count+=1
				self.boucle1=True
				self.t=rospy.get_time()
			elif v1>self.dist_max and v2>self.dist_max  and v3<self.dist_max and (v4 <self.dist_max or v5<self.dist_max )and v3>self.dist_min1 and v4 >self.dist_min1 and v5>self.dist_min2:
				self.lx=self.vit1
				self.az=1.0
				self.count+=1
				self.boucle2=True
				self.t=rospy.get_time()
			elif  v2<self.dist_max  and v3>self.dist_max and v4 >self.dist_max and v5>self.dist_max and v1 >self.dist_min2 and v2>self.dist_min1:
				self.lx=self.vit2
				self.az=-1.0
				self.count+=1
				self.boucle3=True
				self.t=rospy.get_time()
			elif v1>self.dist_max and v2>self.dist_max  and v3>self.dist_max and v4 <self.dist_max and v4 >self.dist_min1 and v5>self.dist_min2:
				self.lx=self.vit2
				self.az=1.0
				self.count+=1
				self.boucle4=True
				self.t=rospy.get_time()
			elif v1<self.dist_max and v2>self.dist_max and v3>self.dist_max and v4>self.dist_max and v5>self.dist_max and v1>self.dist_min2:
				self.lx=self.vit3
				self.az=-1.0
				self.count+=1
				self.boucle5=True
				self.t=rospy.get_time()
			elif v1>self.dist_max and v2>self.dist_max and v3>self.dist_max and v4>self.dist_max and v5<self.dist_max and v5>self.dist_min2:
				self.lx=self.vit3
				self.az=1.0
				self.count+=1
				self.boucle6=True
				self.t=rospy.get_time()
			else:
				self.end=True
			temp=rospy.get_time()-self.t
			print temp
			#and v3>=self.dist_min1 
			if self.end and self.count>0 and temp>2.0 :
				if self.boucle1 and v1>=self.dist_max and v2>=self.dist_max   and v4 >=self.dist_min1 and v5>=self.dist_min2:
					self.lx=self.vit1
					self.az=1.0
					self.count-=1
				elif self.boucle2 and v1>=self.dist_min2  and v2>=self.dist_min1   and v4 >=self.dist_max and v5>=self.dist_max :
					self.lx=self.vit1
					self.az=-1.0
					self.count-=1
				elif self.boucle3 and v1>=self.dist_max  and v2>=self.dist_max   and v4 >=self.dist_min1 and v5>=self.dist_min2:
					self.lx=self.vit2
					self.az=1.0
					self.count-=1
				elif self.boucle4 and v1>=self.dist_min2  and v2>=self.dist_min1   and v4 >=self.dist_max and v5>=self.dist_max:
					self.lx=self.vit2
					self.az=-1.0
					self.count-=1
				elif self.boucle5 and v1>=self.dist_max  and v2>=self.dist_min1   and v4 >=self.dist_min1 and v5>=self.dist_min2:
					self.lx=self.vit3
					self.az=1.0
					self.count-=1
				elif self.boucle6	and v1>=self.dist_min2  and v2>=self.dist_min1  and v4 >=self.dist_min1 and v5>=self.dist_max:
					self.lx=self.vit3
					self.az=-1.0
					self.count-=1
		if self.count==0 or self.twist.angular.z !=0 or self.twist.linear.x<=0 or (self.boucle1 and self.boucle2) or (self.boucle1 and self.boucle3) or (self.boucle1 and self.boucle4) or (self.boucle1 and self.boucle5) or (self.boucle1 and self.boucle6) or (self.boucle2 and self.boucle3) or (self.boucle2 and self.boucle4) or (self.boucle2 and self.boucle5)  or (self.boucle2 and self.boucle6) or (self.boucle3 and self.boucle4) or (self.boucle3 and self.boucle5) or (self.boucle3 and self.boucle6) or (self.boucle4 and self.boucle5) or (self.boucle4 and self.boucle6) or (self.boucle5 and self.boucle6):
			self.boucle1=False
			self.boucle2=False
			self.boucle3=False
			self.boucle4=False
			self.boucle5=False
			self.boucle6=False
			self.end=False
			self.count=0
		print self.count
		self.twist.linear.x=self.lx
		self.twist.angular.z=self.az
		rospy.loginfo("control : x : %s z : %s ",self.twist.linear.x,self.twist.angular.z)
		self.pub.publish(self.twist)
	def callback(self, data):
		#rospy.loginfo("L x : %s, L y : %s,L z : %s ; /t A x : %s, A y : %s, A z : %s \n",data.linear.x,data.linear.y,data.linear.z, data.angular.x,data.angular.y,data.angular.z)
		#global twist
		self.twist=data
	def us1(self,val):
		#print rospy.get_name(), "US1=%s "%str(val.range)
		#global s1
		#global seq
		self.s1=val.range	
	def us2(self,val):
		#print rospy.get_name(), "US2=%s "%str(val.range)
		#global s2
		self.s2=val.range
	def us3(self,val):
		#print rospy.get_name(), "US3=%s "%str(val.range)
		#global s3
		self.s3=val.range
	def us4(self,val):
		#print rospy.get_name(), "US4=%s "%str(val.range)
		#global s4
		self.s4=val.range
	def us5(self,val):
		#print rospy.get_name(), "US5=%s "%str(val.range)
		#global s5
		self.s5=val.range
	def ir1(self,val):
		#print rospy.get_name(), "IR1=%s "%str(val.range)
		#global r1
		self.r1=val.range
	def ir2(self,val):
		#print rospy.get_name(), "IR2=%s "%str(val.range)
		#global r2
		self.r2=val.range
	def ir3(self,val):
		#print rospy.get_name(), "IR3=%s "%str(val.range)
		#global r3
		self.r3=val.range
	def ir4(self,val):
		#print rospy.get_name(), "IR4=%s "%str(val.range)
		#global r4
		self.r4=val.range
	def ir5(self,val):
		#print rospy.get_name(), "IR5=%s "%str(val.range)
		#global r5
		self.r5=val.range
		
#=======================================================================
#self.twist=Twist()
#self.az=self.lx=self.s1=self.s2=self.s3=self.s4=self.s5=self.r1=self.r2=self.r3=self.r4=self.r5=0.0
#try:
rospy.init_node('safe_teleop', anonymous=False)
node=avoider()
r=rospy.Rate(10)
while not rospy.is_shutdown():
	node.control()
	r.sleep()
#rospy.Subscriber('cmd_vel_in', Twist,callback)
#rospy.loginfo("control : x : %s z : %s ",twist.linear.x,twist.angular.z)
#rospy.spin()
#control()
#except rospy.ROSInterruptException:
#pass
